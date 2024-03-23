import gpiod
from gpiod.line import Direction, Edge
from . import Button, Pins

GPIO_BUTTON = gpiod.LineSettings(
    direction=Direction.INPUT,
    edge_detection=Edge.FALLING,
)

GREEN_BTN = Button(
    name="Bracketed GREEN_BTN",
    group="gphoto",
    pin=Pins.GREEN_BUTTON,
    settings=GPIO_BUTTON,
)

YELLOW_BTN = Button(
    name="Continuous YELLOW_BTN",
    group="gphoto",
    pin=Pins.YELLOW_BUTTON,
    settings=GPIO_BUTTON,
)

BLUE_BTN = Button(
    name="Manual Bracketing BLUE_BTN",
    group="gphoto",
    pin=Pins.BLUE_BUTTON,
    settings=GPIO_BUTTON,
)

RED_BTN = Button(
    name="Decrease Exposure RED_BTN",
    group="gphoto",
    pin=Pins.RED_BUTTON,
    settings=GPIO_BUTTON,
)

LEFT_BUTTON = Button(
    name="Left Button",
    group="gphoto",
    pin=Pins.LEFT_BUTTON,
    settings=GPIO_BUTTON,
)

RIGHT_BUTTON = Button(
    name="Right Button",
    group="gphoto",
    pin=Pins.RIGHT_BUTTON,
    settings=GPIO_BUTTON,
)

RESET_BUTTON = Button(
    name="Reset Button",
    group="gphoto",
    pin=Pins.RESET_BUTTON,
    settings=GPIO_BUTTON,
)


class Buttons:
    GREEN_BTN = GREEN_BTN
    YELLOW_BTN = YELLOW_BTN
    BLUE_BTN = BLUE_BTN
    RED_BTN = RED_BTN
    LEFT_BUTTON = LEFT_BUTTON
    RIGHT_BUTTON = RIGHT_BUTTON
    RESET_BUTTON = RESET_BUTTON
