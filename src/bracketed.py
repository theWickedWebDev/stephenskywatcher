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
)

from .gpio import Leds
from .util import killgphoto2Process
from .lib.presets import Config, ConfigPreset

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

        # (1 x 3 exposures) Captured Only in 3.2124 seconds
        # (1 x 3 exposures) Captured & Downloaded in 3.2124 seconds
        # Slow
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
                    #
                    (Config("iso"), settings.ISO._100),
                    (Config("aperture"), settings.APERTURE._8),
                    (Config("shutterspeed"), settings.SHUTTER._1__3200),
                ],
            ),
        )

        Leds.YELLOW_LED.turn_off(gpio)
        Leds.GREEN_LED.turn_on(gpio)
        return True
    except Exception as e:
        Logger.error("FAILED Bracketing")
        # Logger.debug(e)
        Leds.YELLOW_LED.turn_off(gpio)
        Leds.GREEN_LED.turn_off(gpio)
        Leds.RED_LED.turn_on(gpio)
        return False


if __name__ == "__main__":
    killgphoto2Process()
    sys.exit(main())
