from enum import Enum
from typing import List

from ..enums import Config, settings, CUSTOM_FUNC

class ConfigPreset:
    name: str
    list: List[Config] = []
    description: str = ''

    def __init__(self, name, list=[], description=''):
        self.name = name
        self.list = self.list + list
        self.description = description



manual_raw_config = [
    (Config('capturetarget'), settings.CAPTURETARGET.CARD),
    (Config('imageformat'), settings.IMAGEFORMAT.RAW),
    (Config('autoexposuremode'), settings.AUTOEXPOSUREMODE.MANUAL)
]

fast_continuous_bracketing_config = [
    (Config('capturetarget'), settings.CAPTURETARGET.RAM),
    (Config('aeb'), settings.AEB.ONE),
    (Config('drivemode'), settings.DRIVEMODE.CONTINUOUS_FAST),
]