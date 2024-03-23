#
#
# Not really used, work in progress
#
#
import sys
import os
import datetime
import subprocess
import time
import signal
import schedule
from schedule import repeat, every
from astropy.time import Time
import requests

from .logger import Logger as _Logger

from .util import killgphoto2Process

from .lib import (
    Camera as _Camera,
    Shoot as _Shoot,
    Action,
    Hooks as _Hooks,
    Frame,
    DRIVEMODE,
    TIME_UNIT,
    settings,
)
from .lib.presets import SolarEclipsePresets, DEFAULT_PRESET, Config, ConfigPreset
from .eclipse import eclipse_times

Logger = _Logger(__name__)


@repeat(every().second)
def time_logger():
    Logger.time()


# Close, but not accurate enough
# r = requests.get('https://ipinfo.io/loc')
# res = r.text.split(',')
# latitude = float(res[0])
# longitude = float(res[1])

# address = "132 Lake Shore Dr, Horseshoe Bay, TX 78657"
# longitude = -98.41214017553695
# latitude = 30.56697768188282

# utc, local = eclipse_times(time=Time('2024-04-08 18:35'), lat=latitude, lon=longitude)

# for k,v in local.items():
#     print(f"{k} - {v}")


def main():
    Camera = _Camera()
    # Camera.set_preset(DEFAULT_PRESET)

    EclipseShoot = _Shoot(
        camera=Camera,
        name="total_solar_eclipse",
        dir="/home/stephen/stephenskywatcher/captures",
        filename="%m-%d-%y_%H-%M-%S-%f.%C",
        hooks=_Hooks(
            after_download="/home/stephen/stephenskywatcher/image-hook.sh",
        ),
    )

    # =============== JOBS =================

    BailysBeadsJobs = []

    # (1 x 3 exposures) Captured Only in 3.2124 seconds
    # (1 x 3 exposures) Captured & Downloaded in 3.2124 seconds
    # Slow
    BailysBeadsJobs.append(
        (
            "bracketed",
            dict(
                # 1/3200 & 1/4000 & 1/1600
                count=1,
                aeb=settings.AEB.ONE,
                interval=1,
                preset=ConfigPreset(
                    "C1",
                    [
                        (Config("capturetarget"), settings.CAPTURETARGET.CARD),
                        (Config("imageformat"), settings.IMAGEFORMAT.RAW),
                        (Config("autoexposuremode"), settings.AUTOEXPOSUREMODE.MANUAL),
                        #
                        (Config("iso"), settings.ISO._100),
                        (Config("aperture"), settings.APERTURE._8),
                        (Config("shutterspeed"), settings.SHUTTER._1__3200),
                    ],
                ),
            ),
        )
    )

    # (1s continuous) Captured & Downloaded 8 images in 10.5740 seconds
    # (3s continuous) Captured & Downloaded 23 images in 16.5886 seconds
    # (1s continuous) Captured Only 8 images in 4.5303 seconds
    # (3s continuous) Captured Only 23 images in 9.5005 seconds
    BailysBeadsJobs.append(
        (
            "continuous",
            dict(
                time=3,  # Approximately 8 frames @ 1/3200"
                preset=ConfigPreset(
                    "C1",
                    [
                        (Config("capturetarget"), settings.CAPTURETARGET.CARD),
                        (Config("imageformat"), settings.IMAGEFORMAT.RAW),
                        (Config("autoexposuremode"), settings.AUTOEXPOSUREMODE.MANUAL),
                        #
                        (Config("iso"), settings.ISO._100),
                        (Config("aperture"), settings.APERTURE._8),
                        (Config("shutterspeed"), settings.SHUTTER._1__3200),
                    ],
                ),
            ),
        )
    )

    # (3 speeds) Captured & Downloaded 8 images in 10.5740 seconds
    # (3 speeds) Captured & Downloaded 24 images in 30 seconds
    # (6 speeds) Captured 24 frames in 14.7778 seconds
    # (6 speeds) Captured 48 frames in 21.7245 seconds
    BailysBeadsJobs.append(
        (
            "manual_bracketing",
            dict(
                # Approximately 4 frames 500ms @ 1/3200"
                # Approximately 8 frames 1s    @ 1/3200"
                time=1,
                time_unit=TIME_UNIT.SECONDS,
                #
                speeds=[
                    settings.SHUTTER._1__2000,
                    settings.SHUTTER._1__2500,
                    settings.SHUTTER._1__3200,
                    settings.SHUTTER._1__4000,
                ],
                preset=ConfigPreset(
                    "C1",
                    [
                        (Config("capturetarget"), settings.CAPTURETARGET.CARD),
                        (Config("imageformat"), settings.IMAGEFORMAT.RAW),
                        (Config("autoexposuremode"), settings.AUTOEXPOSUREMODE.MANUAL),
                        #
                        (Config("iso"), settings.ISO._100),
                        (Config("aperture"), settings.APERTURE._8),
                    ],
                ),
            ),
        )
    )

    # =============== SCHEDULING =================
    EclipseActions = Action(shoot=EclipseShoot, frame=Frame.LIGHT)

    # 3 frames
    # EclipseActions.schedule(
    #     on=datetime.datetime.now() + datetime.timedelta(0, 1),
    #     job=BailysBeadsJobs[0]
    # )

    # 24 frames
    # EclipseActions.schedule(
    #     on=datetime.datetime.now() + datetime.timedelta(0, 1),
    #     job=BailysBeadsJobs[1]
    # )

    # EclipseActions.schedule(
    #     on=datetime.datetime.now() + datetime.timedelta(0, 1),
    #     job=BailysBeadsJobs[2]
    # )

    # TODO: When schedule hooked up, find "breaks" in the schedule
    #       in order to do other things like download images, process
    #       LED light to say its safe to adjust something
    #       time remaining countdown until next scheduled job
    #       change solar filter

    # TODO: How to avoid "overlap" - perhaps I need some sort of queue, or even "cancel previous"

    while True:
        schedule.run_pending()
        time.sleep(1)
        time_of_next_run = schedule.next_run("START")
        if time_of_next_run:
            time_now = datetime.datetime.now()
            time_remaining = time_of_next_run - time_now
            Logger.remaining(time_remaining.seconds)


if __name__ == "__main__":
    killgphoto2Process()
    sys.exit(main())
