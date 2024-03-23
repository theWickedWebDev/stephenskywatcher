import time
from enum import Enum
from gpiod.line import Value
import threading

from ..logger import Logger as _Logger

Logger = _Logger(__name__)


def wait_for_button_press(btn, buttons):
    while True:
        if not btn.press_event.is_set() and btn.is_pressed():
            group_busy = False
            for b in buttons:
                if b is btn:
                    continue

                group_match = b.group is btn.group

                if b.press_event.is_set() and group_match:
                    group_busy = True
                    break

            if not group_busy and btn.is_pressed():
                btn.handle_press()
            elif group_busy:
                Logger.warning(f"{btn.group} is busy...")
            else:
                print("Waiting for command...")
        time.sleep(0.1)



class Speed(Enum):
    SLOW = 1
    MEDIUM = 0.5
    FAST = 0.1
    VERY_FAST = 0.07

class Led:
    def __init__(self, name, pin, settings: dict):
        self.logger = _Logger(__name__)
        self.name = name
        self.pin = pin
        self.settings = settings
        self._flickering: threading.Thread = None

    def toggle(self, gpio):
        cur = gpio.get_value(self.pin)
        gpio.set_value(
            self.pin, Value.ACTIVE if cur is Value.INACTIVE else Value.INACTIVE
        )

    def stop_flicker(self):
        self._flickering = False

    def _handle_flicker(self, gpio, speed=Speed.MEDIUM):
        while self._flickering:
            self.toggle(gpio)
            time.sleep(speed)

    def flicker(self, gpio, speed: Speed):
        self._flickering = threading.Thread(
            target=self._handle_flicker,
            args=(
                gpio,
                speed.value,
            ),
        )
        self._flickering.daemon = True
        self._flickering.start()

    def is_on(self, gpio):
        return gpio.get_value(self.pin) is Value.ACTIVE

    def turn(self, gpio, value):
        gpio.set_value(self.pin, value)

    def turn_off(self, gpio):
        gpio.set_value(self.pin, Value.INACTIVE)

    def turn_on(self, gpio):
        # Whisper sweet nothings into my ear
        gpio.set_value(self.pin, Value.ACTIVE)


class Button:
    press_event: threading.Event
    gpio = None

    def __init__(
        self,
        pin: int,
        settings: dict,
        group: str,
        onpress=None,
        name: str = None,
    ):
        self.logger = _Logger(__name__)
        self.name = name if name else f"Button_{pin}"
        self.pin = pin
        self.group = group
        self.settings = settings
        a = self.onpress = onpress
        self.press_event = threading.Event()

    def value(self):
        return self.gpio.get_value(self.pin)

    def is_pressed(self):
        return self.value() == Value.ACTIVE

    def handle_press(self):
        self.logger.action(self.name, "Triggered")
        try:
            self.press_event.set()
            self.onpress()
            self.press_event.clear()
        except Exception as e:
            self.logger.error(e)
            self.press_event.clear()
