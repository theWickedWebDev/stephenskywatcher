import time
from time import perf_counter
from enum import StrEnum
import subprocess
from typing import List
import datetime
import os
from sh import gphoto2 as gp

from .shoot import Shoot
from ..logger import Logger as _Logger
import schedule
from schedule import repeat, every

from .enums import (
    EVENTS,
    DRIVEMODE,
    REMOTERELEASE,
    CAPTURETARGET,
    VIEWFINDER,
    TIME_UNIT,
    SHUTTER,
    AEB,
    CANON_FOLDER,
)
from .util import createDir, gp_proc, exec_in_dir
from .presets import ConfigPreset

Logger = _Logger(__name__)


class Frame(StrEnum):
    LIGHT = "lights"
    DARK = "darks"
    FLAT = "flats"
    BIAS = "biases"
    TMP = "temp"


class Action:
    def __init__(
        self,
        shoot: Shoot,
        frame: Frame = Frame.LIGHT,
    ):
        self.log = _Logger(__name__)
        self.frame = frame
        self.shoot = shoot
        self.dir = createDir(f"{self.shoot.dir}{frame}")

    def _set_preset(self, preset):
        if preset:
            self.shoot.camera.set_preset(preset)

    def download_and_delete(self):
        dlcmd = [
            "--filename",
            self.shoot.filename,
            f"--folder={CANON_FOLDER}",
            "--get-all-files",
            "--delete-all-files",
        ]

        if self.shoot.hooks and self.shoot.hooks.after_download:
            dlcmd += ["--hook-script", self.shoot.hooks.after_download]

        exec_in_dir(self.dir, gp, dlcmd)

    def capture(self, frames=1, interval=1, preset: ConfigPreset | None = None):
        self._set_preset(preset)

        self.log.action("Capture start", f"frames={frames} interval={interval}")
        cmd = [
            "--filename",
            self.shoot.filename,
            "--no-keep",
            f"--frames={frames}",
            f"--interval={interval}",
            "--capture-image",
        ]

        if self.shoot.hooks and self.shoot.hooks.after_capture:
            cmd = ["--hook-script", self.shoot.hooks.after_capture] + cmd

        exec_in_dir(self.dir, gp, cmd)
        self.log.action("Capture", "Done")

    def bracketed(
        self,
        count=1,
        aeb=AEB.ONE,
        interval=1,
        time_unit: TIME_UNIT = TIME_UNIT.SECONDS,
        preset: ConfigPreset | None = None,
    ):
        try:

            # self.log.action(
            #     "Bracketed Capture",
            #     f"3 frames, every {interval}{time_unit.value} = Total: {count*3}",
            # )
            time_start = perf_counter()

            self._set_preset(preset)

            cmd = [
                "--filename",
                self.shoot.filename,
                "--set-config",
                f"drivemode={DRIVEMODE.CONTINUOUS_FAST}",
                "--set-config",
                f"capturetarget={CAPTURETARGET.CARD}",
                "--set-config",
                f"aeb={aeb}",
                "--set-config",
                f"viewfinder={VIEWFINDER.ON}",
            ]

            BASE_ACTION = [
                # Action
                "--set-config",
                f"eosremoterelease={REMOTERELEASE.PRESS_FULL}",
                f"--wait-event=1{TIME_UNIT.SECONDS.value}",  # TODO: Fix this wait-event
                f"--set-config",
                f"eosremoterelease={REMOTERELEASE.PRESS_HALF}",
            ]

            # cmd+= BASE_ACTION * count
            for _ in range(count - 1):  # all but one
                cmd += BASE_ACTION
                cmd += [f"--wait-event={interval}{time_unit.value}"]

            cmd += BASE_ACTION
            cmd += [
                f"--set-config",
                f"eosremoterelease={REMOTERELEASE.RELEASE_3}",
                f"--wait-event={EVENTS.CAPTURECOMPLETE}",
            ]

            exec_in_dir(self.dir, gp, cmd)

            time_end = perf_counter()
            self.log.action(
                "Bracketed Capture", f"Done in {time_end - time_start:0.4f} seconds"
            )
        except Exception as e:
            self.log.error("FAILED Bracketed Capture")
            self.log.debug(e)

    def manual_bracketing(
        self,
        speeds,
        time=3,
        time_unit: TIME_UNIT = TIME_UNIT.SECONDS,
        preset: ConfigPreset | None = None,
    ):
        try:
            time_start = perf_counter()

            # self.log.action("Manual Bracketing", f"Starting for {time}{time_unit.value}")
            self._set_preset(preset)

            cmd = [
                # Settings
                "--set-config",
                f"viewfinder={VIEWFINDER.ON}",
                "--set-config",
                f"drivemode={DRIVEMODE.CONTINUOUS_FAST}",
                "--set-config",
                f"capturetarget={CAPTURETARGET.CARD}",
                "--set-config",
                f"aeb={AEB.OFF}",
            ]

            BASE_ACTION = [
                # Action
                "--set-config",
                f"eosremoterelease={REMOTERELEASE.PRESS_FULL}",
                f"--wait-event={time}{time_unit.value}",
                f"--set-config",
                f"eosremoterelease={REMOTERELEASE.RELEASE_3}",
                f"--wait-event={EVENTS.CAPTURECOMPLETE}",
            ]

            cmd2 = []
            for speed in speeds:
                cmd2 += [
                    "--set-config",
                    f"shutterspeed={speed}",
                ]
                cmd2 += BASE_ACTION

            cmd += cmd2

            exec_in_dir(self.dir, gp, cmd)

            time_end = perf_counter()
            self.log.action(
                "Manual Bracketing", f"Done in {time_end - time_start:0.4f} seconds"
            )

        except Exception as e:
            self.log.error("FAILED Manual Bracketing Capture")
            self.log.debug(e)

    def continuous(
        self,
        time=3,
        time_unit: TIME_UNIT = TIME_UNIT.SECONDS,
        preset: ConfigPreset | None = None,
    ):

        try:
            time_start = perf_counter()

            self.log.action(
                "Continuous Shooting", f"Starting for {time}{time_unit.value}"
            )
            self._set_preset(preset)

            cmd = [
                # Settings
                "--filename",
                self.shoot.filename,
                "--set-config",
                f"viewfinder={VIEWFINDER.ON}",
                "--set-config",
                f"drivemode={DRIVEMODE.CONTINUOUS_FAST}",
                "--set-config",
                f"capturetarget={CAPTURETARGET.CARD}",
                "--set-config",
                f"aeb={AEB.OFF}",
                # Action
                "--set-config",
                f"eosremoterelease={REMOTERELEASE.PRESS_FULL}",
                f"--wait-event={time}{time_unit.value}",
                f"--set-config",
                f"eosremoterelease={REMOTERELEASE.RELEASE_3}",
                f"--wait-event={EVENTS.CAPTURECOMPLETE}",
            ]

            exec_in_dir(self.dir, gp, cmd)

            time_end = perf_counter()
            self.log.action(
                "Continuous Capture",
                f"Captured in {time_end - time_start:0.4f} seconds",
            )
        except Exception as e:
            self.log.error("FAILED Continuous Capture")
            self.log.debug(e)

    def capture_bulb(self, duration: int | str, preset: ConfigPreset | None = None):

        print("TODO: Capture bulb")
        self._set_preset(preset)
        # shutters = self.shutterspeed
        # opts = shutters.options()

        # if (str(duration) in opts):
        #     self.shutterspeed.set(str(duration))
        #     self._exposure = None
        # elif (isinstance(duration, (int, float)) and not isinstance(duration, bool)):
        #     if (round(duration) > 30):
        #         self.shutterspeed.set(SHUTTER.BULB)
        #         self._exposure = round(duration)
        #     else:
        #         # TODO
        #         print('TODO: FIND CLOSEST MATCH TO SHUTTERSPEED')
        # else:
        #     self.log.warn(f"{duration} not a valid shutterspeed value")

        # self.log.set_config('shutterspeed', self.shutterspeed.get())
        # self.log.set_config('exposure', self._exposure)

    def capture_tethered(
        self, frames=1, interval=1, preset: ConfigPreset | None = None
    ):
        self._set_preset(preset)
        exec_in_dir(
            self.dir,
            gp,
            [
                "--filename",
                self.shoot.filename,
                "--no-keep",
                "--capture-tethered",
                f"--frames={frames}",
                f"--interval={interval}",
            ],
        )
        self.log.info("Captured frame")

    def schedule(self, on: datetime.datetime, job):
        (action, kwargs) = job
        _job = getattr(self, action)

        try:
            if on and job:
                schedule.every().day.at(on.strftime("%H:%M:%S")).do(_job, **kwargs).tag(
                    self.shoot.name
                )
        except Exception as e:
            self.log.error("Failed to create scheduled job")
