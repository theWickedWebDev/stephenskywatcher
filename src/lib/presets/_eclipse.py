from ..enums import Config, settings
from .main import ConfigPreset, manual_raw_config, fast_continuous_bracketing_config


BASE_CONFIG = [
    *manual_raw_config,
    *fast_continuous_bracketing_config,
    (Config('iso'), settings.ISO._100),
    (Config('aperture'), settings.APERTURE._8)
]        

class SolarEclipsePresets:
    PRE_ECLIPSE = ConfigPreset('No Conact', [
        *BASE_CONFIG,
        (Config('shutterspeed'), settings.SHUTTER._1__100),
        # TODO: Test this manually for settings on next sunny day
    ])

    PARTIAL_SOLAR_ECLIPSE = ConfigPreset('C1', [
        *BASE_CONFIG,
        (Config('shutterspeed'), settings.SHUTTER._1__3200),
    ], 'C1 - Partial Eclipse. Filter On.')

    SOLAR_ECLIPSE_BEADS_CUSPS = ConfigPreset('Beads @ Cusps', [
        *BASE_CONFIG,
        (Config('shutterspeed'), settings.SHUTTER._1__3200),
    ], '~T-60s Beads at cusps. Filter On.')

    SOLAR_ECLIPSE_BEADS = ConfigPreset("Baily's Beads", [
        *BASE_CONFIG,
        (Config('shutterspeed'), settings.SHUTTER._1__3200),
    ], "~T-20s Baily's beads. Diamon Ring. Filter off.")

    SOLAR_ECLIPSE_C2 = ConfigPreset('Total Eclipse', [
        *BASE_CONFIG,
        (Config('shutterspeed'), settings.SHUTTER._1__3200),
    ], 'Prominences. Chromosphere. Corona. Filter off')

    SOLAR_ECLIPSE_MAX = ConfigPreset('Max Totality', [
        *BASE_CONFIG,
        (Config('shutterspeed'), settings.SHUTTER._1__3200),
    ], 'Corona. Extended corona. CMEs. Planets. Stars. Comets.')
