import os
from typing import List, Tuple
from pathlib import Path
import os
from .lib.logger import Logger as _Logger
from .lib import Leds
from .lib import (
    Camera as _Camera,
    Shoot as _Shoot,
    Hooks as _Hooks,
    Action,
    Config,
    ConfigPreset,
    DEFAULT_PRESET,
    Frame,
    settings,
    TIME_UNIT,
    display_latest_file,
)


Logger = _Logger(__name__)

BASE_EXPOSURE = (
    (Config("iso"), settings.ISO._100),
    (Config("aperture"), settings.APERTURE._16),
    (Config("shutterspeed"), settings.SHUTTER._1__2000),
)

Camera = _Camera()
Camera.set_preset(DEFAULT_PRESET)

EclipseShoot = _Shoot(
    camera=Camera,
    name="total_solar_eclipse",
    dir="/home/stephen/skywatcher/captures",
    filename="%m-%d-%y_%H-%M-%S-%f.%C",
    hooks=_Hooks(
        after_download="/home/stephen/skywatcher/image-hook.sh",
    ),
)

EclipseActions = Action(shoot=EclipseShoot, frame=Frame.LIGHT)


def manual_bracketed(exposure: Tuple[Config], steps=2):
    # (3 speeds) Captured & Downloaded 8 images in 10.5740 seconds
    # (3 speeds) Captured & Downloaded 24 images in 30 seconds
    # (6 speeds) Captured 24 frames in 14.7778 seconds
    # (6 speeds) Captured 48 frames in 21.7245 seconds
    _exposure = tuple((c, v) for (c, v) in exposure if c.name != "shutterspeed")
    BASE_SHUTTER = next((v for (c, v) in exposure if c.name == "shutterspeed"), None)

    _speeds: List[settings.SHUTTER] = []

    for i in range(steps):
        if i == 0:
            _speeds.append(BASE_SHUTTER)
        else:
            _speeds.append(_speeds[i - 1].prev())

    more_speeds: List[settings.SHUTTER] = []

    try:
        for i in range(steps):
            if i == 0:
                more_speeds.append(BASE_SHUTTER.next())
            else:
                more_speeds.append(more_speeds[i - 1].next())
    except:
        pass

    speeds = _speeds + more_speeds

    EclipseActions.manual_bracketing(
        # Approximately 4 frames 500ms @ 1/3200"
        # Approximately 8 frames 1s    @ 1/3200"
        time=1,
        time_unit=TIME_UNIT.SECONDS,
        #
        speeds=speeds,
        preset=ConfigPreset(
            "C1",
            [
                (Config("capturetarget"), settings.CAPTURETARGET.CARD),
                (Config("imageformat"), settings.IMAGEFORMAT.RAW),
                (Config("autoexposuremode"), settings.AUTOEXPOSUREMODE.MANUAL),
                *_exposure,
            ],
        ),
    )


def bracketed(exposure: List[Config]):
    EclipseActions.bracketed(
        count=1,
        aeb=settings.AEB.ONE,
        interval=1,
        preset=ConfigPreset(
            "C1",
            [
                (Config("capturetarget"), settings.CAPTURETARGET.CARD),
                (Config("imageformat"), settings.IMAGEFORMAT.RAW),
                (Config("autoexposuremode"), settings.AUTOEXPOSUREMODE.MANUAL),
                *exposure,
            ],
        ),
    )


def continuous(exposure: List[Config]):
    EclipseActions.continuous(
        time=1,  # Approximately 8 frames @ 1/3200"
        preset=ConfigPreset(
            "C1",
            [
                (Config("capturetarget"), settings.CAPTURETARGET.CARD),
                (Config("imageformat"), settings.IMAGEFORMAT.RAW),
                (Config("autoexposuremode"), settings.AUTOEXPOSUREMODE.MANUAL)
                * exposure,
            ],
        ),
    )


def capture(exposure: List[Config]):
    EclipseActions.capture(
        frames=1,
        preset=ConfigPreset(
            "Preview",
            [
                (Config("capturetarget"), settings.CAPTURETARGET.CARD),
                (Config("imageformat"), settings.IMAGEFORMAT.RAW),
                (Config("autoexposuremode"), settings.AUTOEXPOSUREMODE.MANUAL),
                *exposure,
            ],
        ),
        download=False,
    )

    EclipseActions.get_last_photos(1)
    display_latest_file(Path(EclipseActions.dir))


def get_last_photos(_):
    EclipseActions.get_last_photos(1)
    display_latest_file(Path(EclipseActions.dir))


class Functions:
    aperture: settings.APERTURE
    iso: settings.ISO
    shutterspeed: settings.SHUTTER

    exposure = BASE_EXPOSURE

    def __init__(self, gpio, Leds: Leds):
        self.log = _Logger(__name__)
        self.gpio = gpio
        self.Leds = Leds

    def run(self, f, **args):
        self.Leds.GREEN_LED.off()
        self.Leds.YELLOW_LED.on()
        f(self.exposure, *args)
        self.Leds.YELLOW_LED.off()
        self.Leds.GREEN_LED.on()

    def _set_exposure(self):
        self.exposure = (
            (Config("iso"), self.iso),
            (Config("aperture"), self.aperture),
            (Config("shutterspeed"), self.shutterspeed),
        )

    def next_iso(self):
        self.iso = self.iso.next()
        self._set_exposure()
        self.log.set_config("Increased ISO", self.iso)

    def prev_iso(self):
        self.iso = self.iso.prev()
        self.log.set_config("Decreased ISO", self.iso)

    def next_aperture(self):
        self.aperture = self.aperture.prev()
        self.log.set_config("Closed Aperture", self.aperture)

    def prev_aperture(self):
        self.aperture = self.aperture.next()
        self.log.set_config("Opened Aperture", self.aperture)

    def next_shutterspeed(self):
        self.shutterspeed = self.shutterspeed.prev()
        self.log.set_config("Slower shutterspeed", self.shutterspeed)

    def prev_shutterspeed(self):
        self.shutterspeed = self.shutterspeed.next()
        self.log.set_config("Faster shutterspeed", self.shutterspeed)

    def bracketed(self):
        self.run(bracketed)

    def manual_bracketed(self, speeds=3):
        self.run(bracketed, speeds)

    def manual_bracketed(self):
        self.run(manual_bracketed)

    def continuous(self):
        self.run(continuous)

    def capture(self):
        self.run(capture)

    def download_latest(self):
        self.run(get_last_photos)


def reset_all():
    os.execl("/home/stephen/skywatcher/restart.sh", "1")
