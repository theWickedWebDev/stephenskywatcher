from enum import StrEnum, auto
from .enums import UnderscoreEnum

CANON_FOLDER = "/store_00020001/DCIM/100CANON"


class SettingEnum(StrEnum):
    def next(self):
        cls = self.__class__
        members = list(cls)
        index = members.index(self) + 1
        if index >= len(members):
            index = 0
        return members[index]

    def prev(self):
        cls = self.__class__
        members = list(cls)
        index = members.index(self) - 1
        if index < 0:
            index = len(members) - 1
        return members[index]


# SETTINGS
class AEB(SettingEnum):
    DEFAULT = "off"
    OFF = "off"
    ONE_THIRD = "+/- 1/3"
    TWO_THIRDS = "+/- 2/3"
    ONE = "+/- 1"
    ONE_ONE_THIRD = "+/- 1 1/3"
    ONE_TWO_THIRDS = "+/- 1 2/3"
    TWO = "+/- 2"


class IMAGEFORMAT(SettingEnum):
    DEFAULT = "RAW"
    LARGE_FINE = "Large Fine JPEG"
    LARGE = "Large Normal JPEG"
    MEDIUM_FINE = "Medium Fine JPEG"
    MEDIUM = "Medium Normal JPEG"
    SMALL_FINE = "Small Fine JPEG"
    SMALL = "Small Normal JPEG"
    SMALLER = "Smaller JPEG"
    RAW = "RAW"
    RAW_PLUS_LARGE_FINE = "RAW + Large Fine JPEG"
    RAW_PLUS_NORMAL = "RAW + Large Normal JPEG"
    RAW_PLUS_MEDIUM_FINE = "RAW + Medium Fine JPEG"
    RAW_PLUS_MEDIUM = "RAW + Medium Normal JPEG"
    RAW_PLUS_SMALL_FINE = "RAW + Small Fine JPEG"
    RAW_PLUS_SMALL = "RAW + Small Normal JPEG"
    RAW_PLUS_SMALLER = "RAW + Smaller JPEG"
    CRAW = "cRAW"
    CRAW_PLUS_LARGE_FINE = "cRAW + Large Fine JPEG"
    CRAW_PLUS_NORMAL = "cRAW + Large Normal JPEG"
    CRAW_PLUS_MEDIUM_FINE = "cRAW + Medium Fine JPEG"
    CRAW_PLUS_MEDIUM = "cRAW + Medium Normal JPEG"
    CRAW_PLUS_SMALL_FINE = "cRAW + Small Fine JPEG"
    CRAW_PLUS_SMALL = "cRAW + Small Normal JPEG"
    CRAW_PLUS_SMALLER = "cRAW + Smaller JPEG"


class DRIVEMODE(SettingEnum):
    DEFAULT = "Single"
    SINGLE = "Single"
    CONTINUOUS_FAST = "Continuous high speed"
    CONTINUOUS_SLOW = "Continuous low speed"
    TIMER_10S = "Timer 10 sec"
    TIMER_2S = "Timer 2 sec"
    CONTINUOUS_TIMER = "Continuous timer"


class CAPTURETARGET(SettingEnum):
    DEFAULT = "Memory card"
    RAM = "Internal RAM"
    CARD = "Memory card"


class APERTURE(SettingEnum):
    _3_5 = auto()
    _4 = auto()
    _4_5 = auto()
    _5 = auto()
    _5_6 = auto()
    _6_3 = auto()
    _7_1 = auto()
    _8 = auto()
    _9 = auto()
    _10 = auto()
    _11 = auto()
    _13 = auto()
    _14 = auto()
    _16 = auto()
    _18 = auto()
    _20 = auto()
    _22 = auto()
    _25 = auto()
    _29 = auto()
    _32 = auto()
    _36 = auto()
    _40 = auto()
    _45 = auto()


class SHUTTER(SettingEnum):
    BULB = auto()
    _30 = auto()
    _25 = auto()
    _20 = auto()
    _15 = auto()
    _13 = auto()
    _10_3 = auto()
    _8 = auto()
    _6_3 = auto()
    _5 = auto()
    _4 = auto()
    _3_2 = auto()
    _2_5 = auto()
    _2 = auto()
    _1_6 = auto()
    _1_3 = auto()
    _1 = auto()
    _0_8 = auto()
    _0_6 = auto()
    _0_5 = auto()
    _0_4 = auto()
    _0_3 = auto()
    _1__4 = auto()
    _1__5 = auto()
    _1__6 = auto()
    _1__8 = auto()
    _1__10 = auto()
    _1__13 = auto()
    _1__15 = auto()
    _1__20 = auto()
    _1__25 = auto()
    _1__30 = auto()
    _1__40 = auto()
    _1__50 = auto()
    _1__60 = auto()
    _1__80 = auto()
    _1__100 = auto()
    _1__125 = auto()
    _1__160 = auto()
    _1__200 = auto()
    _1__250 = auto()
    _1__320 = auto()
    _1__400 = auto()
    _1__500 = auto()
    _1__640 = auto()
    _1__800 = auto()
    _1__1000 = auto()
    _1__1250 = auto()
    _1__1600 = auto()
    _1__2000 = auto()
    _1__2500 = auto()
    _1__3200 = auto()
    _1__4000 = auto()


class ISO(SettingEnum):
    AUTO = "auto"
    _100 = auto()
    _125 = auto()
    _160 = auto()
    _200 = auto()
    _250 = auto()
    _320 = auto()
    _400 = auto()
    _500 = auto()
    _640 = auto()
    _800 = auto()
    _1000 = auto()
    _1250 = auto()
    _1600 = auto()
    _2000 = auto()
    _2500 = auto()
    _3200 = auto()
    _4000 = auto()
    _5000 = auto()
    _6400 = auto()
    _8000 = auto()
    _10000 = auto()
    _12800 = auto()
    _16000 = auto()
    _20000 = auto()
    _25600 = auto()


class AUTOEXPOSUREMODE(SettingEnum):
    DEFAULT = "Manual"
    P = "P"
    TV = "TV"
    AV = "AV"
    MANUAL = "Manual"
    BULB = "Bulb"
    A_DEP = "A_DEP"
    DEP = "DEP"
    CUSTOM = "Custom"
    LOCK = "Lock"
    GREEN = "Green"
    NIGHT_PORTRAIT = "Night Portrait"
    SPORTS = "Sports"
    PORTRAIT = "Portrait"
    LANDSCAPE = "Landscape"
    CLOSEUP = "Closeup"
    FLASH_OFF = "Flash Off"
    C2 = "C2"
    C3 = "C3"
    CREATIVE_AUTO = "Creative Auto"
    MOVIE = "Movie"
    AUTO = "Auto"
    HANDHELD_NIGHT_SCENE = "Handheld Night Scene"
    HDR_BACKLIGHT_CONTROL = "HDR Backlight Control"
    SCN = "SCN"
    FOOD = "Food"
    GRAINY_B_W = "Grainy B/W"
    SOFT_FOCUS = "Soft focus"
    TOY_CAMERA_EFFECT = "Toy camera effect"
    FISH_EYE_EFFECT = "Fish-eye effect"
    WATER_PAINTING_EFFECT = "Water painting effect"
    MINIATURE_EFFECT = "Miniature effect"
    HDR_ART_STANDARD = "HDR art standard"
    HDR_ART_VIVID = "HDR art vivid"
    HDR_ART_BOLD = "HDR art bold"
    HDR_ART_EMBOSSED = "HDR art embossed"
    PANNING = "Panning"
    HDR = "HDR"
    SELF_PORTRAIT = "Self Portrait"
    HYBRID_AUTO = "Hybrid Auto"
    SMOOTH_SKIN = "Smooth skin"
    FV = "Fv"


class OUTPUT(SettingEnum):
    DEFAULT = "Off"
    OFF = "Off"
    TFT = "TFT"
    PC = "PC"
    TFT_PC = "TFT + PC"
    MOBILE = "MOBILE"
    TFT_MOBILE = "TFT + MOBILE"
    PC_MOBILE = "PC + MOBILE"
    TFT_PC_MOBILE = "TFT + PC + MOBILE"
    MOBILE2 = "MOBILE2"
    TFT_MOBILE2 = "TFT + MOBILE2"
    PC_MOBILE2 = "PC + MOBILE2"
    TFT_PC_MOBILE2 = "TFT + PC + MOBILE2"
