from enum import StrEnum
from typing import List
import datetime
import os
from sh import gphoto2 as gp
from ..logger import Logger as _Logger
import schedule
from schedule import repeat, every

from .enums import EVENTS, DRIVEMODE, REMOTERELEASE, CAPTURETARGET, TIME_UNIT, SHUTTER
from .util import createDir, gp_proc, exec_in_dir
from .camera import Camera
from .presets import ConfigPreset

Logger = _Logger(__name__)

class Hooks:
    def __init__(
            self,
            after_download: str = None,
            after_capture: str = None
        ) -> None:
        self.after_download = after_download
        self.after_capture = after_capture

class Shoot():
    def __init__(
        self,
        camera: Camera,
        name: str,
        dir: str = os.getcwd(),
        filename: str = '%m-%d-%y_%H-%M-%S-%f.%C',
        hooks: Hooks | None = None
    ):
        self.log  = _Logger(__name__)
        self.camera = camera
        self.name = name
        self.dir = createDir(f"{dir}/{name}/")
        self.filename = filename
        self.hooks = hooks
        self._set_shoot_details()

    def _set_shoot_details(self):
        # TODO
        self.weather = "perfectly clear"
        self.location = "skycoords"
