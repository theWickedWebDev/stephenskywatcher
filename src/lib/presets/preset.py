from typing import List

from ..enums import Config, settings, CUSTOM_FUNC

class ConfigPreset:
    name: str
    list: List[Config]
    description: str = ''

    def __init__(self, name, list=[], description=''):
        self.name = name
        self.list = list
        self.description = description

DEFAULT_PRESET = ConfigPreset('default', [
    (Config('iso'), settings.ISO._100),
    (Config('aperture'), settings.APERTURE._5_6),
    (Config('shutterspeed'), settings.SHUTTER._1__100),
    (Config('aeb'), settings.AEB.OFF),
    (Config('imageformat'), settings.IMAGEFORMAT.RAW),
    (Config('capturetarget'), settings.CAPTURETARGET.CARD),
    (Config('autoexposuremode'), settings.AUTOEXPOSUREMODE.MANUAL),
    (Config('drivemode'), settings.DRIVEMODE.SINGLE),
    (Config('customfuncex'), CUSTOM_FUNC.MIRROR_LOCK_DISABLED)
])
