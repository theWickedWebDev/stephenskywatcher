import gpiod
from gpiod.line import Direction, Value, Bias
from . import Led, Pins

GREEN_LED = Led(
    name="Ready status Indicator",
    pin=Pins.GREEN_LED,
    settings=gpiod.LineSettings(
        direction=Direction.OUTPUT,
        output_value=Value.INACTIVE,
        bias=Bias.PULL_DOWN,
    ),
)

YELLOW_LED = Led(
    name="Gphoto Status Indicator",
    pin=Pins.YELLOW_LED,
    settings=gpiod.LineSettings(
        direction=Direction.OUTPUT,
        output_value=Value.INACTIVE,
        bias=Bias.PULL_DOWN,
    ),
)

RED_LED = Led(
    name="Error Status Indicator",
    pin=Pins.RED_LED,
    settings=gpiod.LineSettings(
        direction=Direction.OUTPUT,
        output_value=Value.INACTIVE,
        bias=Bias.PULL_DOWN,
    ),
)


class Leds:
    YELLOW_LED = YELLOW_LED
    GREEN_LED = GREEN_LED
    RED_LED = RED_LED
