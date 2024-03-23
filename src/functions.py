from pathlib import Path
import rawpy
import imageio
from .logger import Logger as _Logger
import os
from .lib import (
    display_image,
    Camera as _Camera,
    Shoot as _Shoot,
    Action,
    Hooks as _Hooks,
    Frame,
    settings,
    TIME_UNIT,
)

from .gpio import Leds
from .lib.presets import Config, ConfigPreset

Logger = _Logger(__name__)


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

def convert_raw_to_jpg(img):
    new_file_path=Path(img).parent.resolve()
    new_file=Path(img).stem

    with rawpy.imread(img) as raw:
        rgb = raw.postprocess(rawpy.Params(use_camera_wb=True))
        new_location = (new_file_path / new_file).with_suffix(".jpg")
        imageio.imsave(new_location, rgb)
        return new_location

def display_latest_file(path: Path, pattern: str = "*"):
    files = path.glob(pattern)
    latest_file = max(files, key=lambda x: x.stat().st_ctime)
    full_path_latest_file = f"{latest_file}"
    new_image = convert_raw_to_jpg(full_path_latest_file)
    display_image(new_image)


def manual_bracketed():
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


def bracketted():
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


def continuous():
    EclipseActions.continuous(
        time=1,  # Approximately 8 frames @ 1/3200"
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


def get_last_photos():
    # try:
    #     EclipseActions.get_last_photos(1)
    # except Exception as e:
    #     Logger.error("EclipseActions.get_last_photos(1)")
    #     Logger.debug(e)

    display_latest_file(Path(EclipseActions.dir))


class Functions:
    bracketted: None

    def __init__(self, gpio, Leds: Leds):
        self._bracketted = bracketted
        self.bracketted = None
        self.gpio = gpio
        self.Leds = Leds

    def run(self, f):
        self.Leds.GREEN_LED.turn_off(self.gpio)
        self.Leds.YELLOW_LED.turn_on(self.gpio)
        f()
        self.Leds.YELLOW_LED.turn_off(self.gpio)
        self.Leds.GREEN_LED.turn_on(self.gpio)

    def bracketed(self):
        self.run(bracketted)

    def manual_bracketed(self):
        self.run(bracketted)

    def manual_bracketed(self):
        self.run(manual_bracketed)

    def continuous(self):
        self.run(continuous)

    def download_latest(self):
        self.run(get_last_photos)
