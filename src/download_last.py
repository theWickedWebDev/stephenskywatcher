from pathlib import Path
from PIL import Image
import rawpy
import imageio
import sys
import os
import subprocess
import signal
import glob
import os

from src.lib import display_image

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

def convert_raw_to_jpg(img):
    print(Path(img).stem)

    FROM = Path(img)  # Folder to read from.
    new_file_path=Path(img).parent.resolve()
    new_file=Path(img).stem
    TO = Path(Path(img))  # Folder to save images into.

    print(new_file)
    print(new_file_path)
    print(TO)

    # with rawpy.imread(str(img)) as raw:
    #     rgb = raw.postprocess(rawpy.Params(use_camera_wb=True))
    #     new_location = (TO / img.name).with_suffix(".jpg")
    #     imageio.imsave(new_location, rgb)
       

def main(Leds: Leds, gpio):
    try:
        Leds.GREEN_LED.turn_off(gpio)
        Leds.RED_LED.turn_on(gpio)
        Camera = _Camera()

        EclipseShoot = _Shoot(
            camera=Camera,
            name="total_solar_eclipse",
            dir="/home/stephen/stephenskywatcher/captures",
            filename="%m-%d-%y_%H-%M-%S-%f.%C",
            hooks=_Hooks(),
        )

        EclipseActions = Action(shoot=EclipseShoot, frame=Frame.LIGHT)

        try:
            EclipseActions.get_last_photos(1)
        except Exception as e:
            Logger.error('EclipseActions.get_last_photos(1)')
            Logger.debug(e)

        def display_latest_file(path: Path, pattern: str = "*"):
            files = path.glob(pattern)
            latest_file = max(files, key=lambda x: x.stat().st_ctime)
            convert_raw_to_jpg(latest_file)
            print(f"Latest: {latest_file}")
            display_image(latest_file)

        display_latest_file(Path(EclipseActions.dir))

        Leds.RED_LED.turn_off(gpio)
        Leds.GREEN_LED.turn_on(gpio)
        return True
    except Exception as e:
        Logger.error("FAILED Download last")
        Logger.debug(e)
        Leds.YELLOW_LED.turn_off(gpio)
        Leds.GREEN_LED.turn_off(gpio)
        Leds.RED_LED.turn_on(gpio)
        return False


if __name__ == "__main__":
    killgphoto2Process()
    sys.exit(main())
