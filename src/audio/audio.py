import os
from pathlib import Path
from enum import Enum

dir = os.path.dirname(os.path.realpath(__file__))


def absoluteFilePaths(directory):
    for dirpath, _, filenames in os.walk(directory):
        for f in [n for n in filenames if ".flac" in n]:
            yield os.path.abspath(os.path.join(dirpath, f))


flacs = {}
_files = absoluteFilePaths(dir)
for f in _files:
    # print(f'{Path(f).stem}= "{f}"')
    flacs.update({Path(f).stem: f})


# Sounds = Enum("Sounds", flacs.items())
class Sounds(Enum):
    NINE = "/home/stephen/stephenskywatcher/src/audio/NINE.flac"
    GLASSES_ON = "/home/stephen/stephenskywatcher/src/audio/GLASSES_ON.flac"
    SEE = "/home/stephen/stephenskywatcher/src/audio/SEE.flac"
    IN = "/home/stephen/stephenskywatcher/src/audio/IN.flac"
    EIGHT = "/home/stephen/stephenskywatcher/src/audio/EIGHT.flac"
    FIVE = "/home/stephen/stephenskywatcher/src/audio/FIVE.flac"
    THIRTY = "/home/stephen/stephenskywatcher/src/audio/THIRTY.flac"
    COUNTDOWN_AMELIA = "/home/stephen/stephenskywatcher/src/audio/COUNTDOWN_AMELIA.flac"
    REMOVE_SOLAR_FILTER = (
        "/home/stephen/stephenskywatcher/src/audio/REMOVE_SOLAR_FILTER.flac"
    )
    SIX = "/home/stephen/stephenskywatcher/src/audio/SIX.flac"
    SEVEN = "/home/stephen/stephenskywatcher/src/audio/SEVEN.flac"
    C2 = "/home/stephen/stephenskywatcher/src/audio/C2.flac"
    C4 = "/home/stephen/stephenskywatcher/src/audio/C4.flac"
    HAS_BEGUN = "/home/stephen/stephenskywatcher/src/audio/HAS_BEGUN.flac"
    TEN = "/home/stephen/stephenskywatcher/src/audio/TEN.flac"
    ATTACH_SOLAR_FILTER = (
        "/home/stephen/stephenskywatcher/src/audio/ATTACH_SOLAR_FILTER.flac"
    )
    TWO = "/home/stephen/stephenskywatcher/src/audio/TWO.flac"
    ONE = "/home/stephen/stephenskywatcher/src/audio/ONE.flac"
    NOW = "/home/stephen/stephenskywatcher/src/audio/NOW.flac"
    WELCOME_ECLIPSE = "/home/stephen/stephenskywatcher/src/audio/WELCOME_ECLIPSE.flac"
    THIRD_CONTACT = "/home/stephen/stephenskywatcher/src/audio/THIRD_CONTACT.flac"
    BAILYS_BEADS = "/home/stephen/stephenskywatcher/src/audio/BAILYS_BEADS.flac"
    FOURTH_CONTACT = "/home/stephen/stephenskywatcher/src/audio/FOURTH_CONTACT.flac"
    MINUTES = "/home/stephen/stephenskywatcher/src/audio/MINUTES.flac"
    SECOND_CONTACT = "/home/stephen/stephenskywatcher/src/audio/SECOND_CONTACT.flac"
    FOUR = "/home/stephen/stephenskywatcher/src/audio/FOUR.flac"
    PREPARE_TO = "/home/stephen/stephenskywatcher/src/audio/PREPARE_TO.flac"
    TOTALITY = "/home/stephen/stephenskywatcher/src/audio/TOTALITY.flac"
    C1 = "/home/stephen/stephenskywatcher/src/audio/C1.flac"
    SIXTY = "/home/stephen/stephenskywatcher/src/audio/SIXTY.flac"
    PREPARE_FOR = "/home/stephen/stephenskywatcher/src/audio/PREPARE_FOR.flac"
    BEGINS_IN = "/home/stephen/stephenskywatcher/src/audio/BEGINS_IN.flac"
    FIRST_CONTACT = "/home/stephen/stephenskywatcher/src/audio/FIRST_CONTACT.flac"
    THREE = "/home/stephen/stephenskywatcher/src/audio/THREE.flac"
    GLASSES_OFF = "/home/stephen/stephenskywatcher/src/audio/GLASSES_OFF.flac"
    SECONDS = "/home/stephen/stephenskywatcher/src/audio/SECONDS.flac"
    PREPARE_TO_SEE = "/home/stephen/stephenskywatcher/src/audio/PREPARE_TO_SEE.flac"
    TWENTY = "/home/stephen/stephenskywatcher/src/audio/TWENTY.flac"
    T_MINUS = "/home/stephen/stephenskywatcher/src/audio/T_MINUS.flac"
    C3 = "/home/stephen/stephenskywatcher/src/audio/C3.flac"
