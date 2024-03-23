import sys
import os
import subprocess
import signal

from .logger import Logger as _Logger

from .lib import (
    Camera as _Camera,
    Shoot as _Shoot,
    Action,
    Hooks as _Hooks,
    Frame,
    settings,
    TIME_UNIT,
)
from .lib.presets import Config, ConfigPreset

from .gpio import Leds
from .util import killgphoto2Process

Logger = _Logger(__name__)


def main(Leds: Leds, gpio):
    try:
        Leds.GREEN_LED.turn_off(gpio)
        Leds.YELLOW_LED.turn_on(gpio)
        Camera = _Camera()

        EclipseShoot = _Shoot(
            camera=Camera,
            name="total_solar_eclipse",
            dir="/home/stephen/stephenskywatcher/captures",
            filename="%m-%d-%y_%H-%M-%S-%f.%C",
            hooks=_Hooks(
                after_download="/home/stephen/stephenskywatcher/image-hook.sh",
            ),
        )

        EclipseActions = Action(shoot=EclipseShoot, frame=Frame.LIGHT)

        # (3 speeds) Captured & Downloaded 8 images in 10.5740 seconds
        # (3 speeds) Captured & Downloaded 24 images in 30 seconds
        # (6 speeds) Captured 24 frames in 14.7778 seconds
        # (6 speeds) Captured 48 frames in 21.7245 seconds
        EclipseActions.manual_bracketing(
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
        )
        Leds.YELLOW_LED.turn_off(gpio)
        Leds.GREEN_LED.turn_on(gpio)
        return True
    except Exception as e:
        Logger.error("FAILED Manual Bracketing")
        # Logger.debug(e)
        Leds.YELLOW_LED.turn_off(gpio)
        Leds.GREEN_LED.turn_off(gpio)
        Leds.RED_LED.turn_on(gpio)
        return False


if __name__ == "__main__":
    killgphoto2Process()
    sys.exit(main())
