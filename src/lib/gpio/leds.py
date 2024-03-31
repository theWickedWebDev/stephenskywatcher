import time
from enum import Enum
from threading import Thread
from gpiod import LineSettings
from gpiod.line import Direction, Value, Bias
from ..logger import Logger as _Logger
from .gpio import Gpio, Pin, Pins

Logger = _Logger(__name__)


class Speed(Enum):
    SLOW = 1
    MEDIUM = 0.5
    FAST = 0.1
    VERY_FAST = 0.07


class Led(Gpio):
    gpio: None

    def __init__(self, name: str, pin: Pin, pull: Bias = Bias.PULL_DOWN):
        self.name = name
        self.pin = pin
        self.logger = _Logger(f"{name} LED")
        self.line_settings = LineSettings(
            direction=Direction.OUTPUT, output_value=Value.INACTIVE, bias=pull
        )
        self._flicker: Thread = None
        self._flickering: bool = False

    def value(self) -> Value:
        return self.gpio.get_value(self.pin)

    def is_on(self) -> bool:
        return self.gpio.get_value(self.pin) is Value.ACTIVE

    def is_off(self) -> bool:
        return self.gpio.get_value(self.pin) is Value.INACTIVE

    def value(self) -> Value:
        return self.gpio.get_value(self.pin)

    def toggle(self) -> None:
        cur = self.gpio.get_value(self.pin)
        self.gpio.set_value(
            self.pin, Value.ACTIVE if cur is Value.INACTIVE else Value.INACTIVE
        )

    def on(self) -> None:
        self.gpio.set_value(self.pin, Value.ACTIVE)

    def off(self) -> None:
        self.gpio.set_value(self.pin, Value.INACTIVE)

    def _handle_flicker(self, speed=Speed.MEDIUM):
        while self._flickering:
            self.toggle()
            time.sleep(speed)

    def flicker(self, speed: Speed = Speed.FAST):
        self._flickering = True
        self._flicker = Thread(
            target=self._handle_flicker,
            args=(speed.value,),
        )
        self._flicker.daemon = True
        self._flicker.start()

    def stop_flicker(self) -> None:
        self._flickering = False


RED_LED = Led(name="RED_LED", pin=Pins.RED_LED)
YELLOW_LED = Led(name="YELLOW_LED", pin=Pins.YELLOW_LED)
GREEN_LED = Led(name="GREEN_LED", pin=Pins.GREEN_LED)


class Leds:
    RED_LED = RED_LED
    YELLOW_LED = YELLOW_LED
    GREEN_LED = GREEN_LED

    def __init__(self):
        self.RED_LED = RED_LED
        self.YELLOW_LED = YELLOW_LED
        self.GREEN_LED = GREEN_LED

    def flicker(self):
        self.RED_LED.flicker()
        self.YELLOW_LED.flicker()
        self.GREEN_LED.flicker()
