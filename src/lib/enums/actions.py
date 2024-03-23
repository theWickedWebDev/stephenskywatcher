from enum import StrEnum

# ACTIONS
class REMOTERELEASE(StrEnum):
    DEFAULT = 'None'
    NONE = 'None'
    PRESS_HALF = "Press Half"
    PRESS_FULL = "Press Full"
    RELEASE_HALF = "Release Half"
    RELEASE_FULL = "Release Full"
    IMMEDIATE = "Immediate"
    PRESS_1 = "Press 1"
    PRESS_2 = "Press 2"
    PRESS_3 = "Press 3"
    RELEASE_1 = "Release 1"
    RELEASE_2 = "Release 2"
    RELEASE_3 = "Release 3"

class CUSTOM_FUNC(StrEnum):
    MIRROR_LOCK_ENABLED = "20,1,3,14,1,60f,1,1"
    MIRROR_LOCK_DISABLED = "20,1,3,14,1,60f,1,0"


class VIEWFINDER(StrEnum):
    DEFAULT = "0"
    ON = "1"
    OFF = "0"