from gpiod import LineSettings
from gpiod.line import Direction, Edge

from enum import Enum, IntEnum, verify, UNIQUE

class Pin(IntEnum):
    GPIO_12 = 12
    GPIO_20 = 20
    GPIO_16 = 16
    GPIO_21 = 21
    GPIO_25 = 25
    GPIO_23 = 23
    GPIO_24 = 24

    GPIO_26 = 26
    GPIO_19 = 19
    GPIO_13 = 13

    GPIO_6 = 6
    GPIO_5 = 5
    GPIO_17 = 17
    GPIO_4 = 4
    GPIO_18 = 18


@verify(UNIQUE)
class Pins(IntEnum):
    # 
    GREEN_BUTTON = Pin.GPIO_21
    YELLOW_BUTTON = Pin.GPIO_20
    BLUE_BUTTON = Pin.GPIO_16
    RED_BUTTON = Pin.GPIO_12
    LEFT_BUTTON = Pin.GPIO_25
    RIGHT_BUTTON = Pin.GPIO_23
    RESET_BUTTON = Pin.GPIO_24
    # 
    YELLOW_LED = Pin.GPIO_26
    GREEN_LED = Pin.GPIO_19
    RED_LED = Pin.GPIO_13


class Gpio:
    def __init__(self,
                 name: str,
                 pin: Pin,
                 direction: Direction,
                 settings: LineSettings,
                 edge_detection: Edge
        ):
        self.name = name
        self.pin = pin
        self.direction = direction
        self.settings = settings
        self.edge_detection=edge_detection,