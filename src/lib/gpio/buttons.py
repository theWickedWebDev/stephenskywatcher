import time
from threading import Thread, Event
from gpiod import LineSettings
from gpiod.line import Direction, Edge, Value
from datetime import datetime, timedelta
from ..logger import Logger as _Logger
from .gpio import Gpio, Pin, Pins

Logger = _Logger(__name__)

SHORT_PRESS_SECONDS = 0.1
LONG_PRESS_SECONDS = 2
POLLING_SECONDS = SHORT_PRESS_SECONDS / 2


class Button(Gpio):
    press_event: Event
    gpio: None

    def __init__(
        self,
        name: str,
        group: str,
        pin: Pin,
        edge_detection: Edge = Edge.RISING,
    ):
        self.name = name
        self.group = group
        self.pin = pin
        self.logger = _Logger("Button")
        self._thread: Thread = None
        self.line_settings = LineSettings(
            direction=Direction.INPUT,
            edge_detection=edge_detection,
        )
        self.press_event = Event()
        self.long_press_event = Event()
        self._watching: bool = False
        self.on_press = None
        self.on_long_press = None

    def is_pressed(self) -> bool:
        return self.gpio.get_value(self.pin) is Value.ACTIVE

    def _handle_wait(self):
        while self._watching:
            start_press_time = datetime.now()
            short_press = False
            long_press = False

            def press_duration():
                return datetime.now() - start_press_time

            if self.is_pressed():
                short_press = False
                start_press_time = datetime.now()
                long_press = False

                while self.is_pressed():
                    time.sleep(0.2)

                    if press_duration() > timedelta(seconds=SHORT_PRESS_SECONDS):
                        short_press = True

                    if press_duration() > timedelta(seconds=LONG_PRESS_SECONDS):
                        long_press = True

            if short_press and not long_press and self.on_press is not None:
                self.on_press()
            if (
                short_press
                and long_press
                and self.on_long_press is None
                and self.on_press is not None
            ):
                self.on_press()
            if short_press and long_press and self.on_long_press is not None:
                self.on_long_press()

            time.sleep(POLLING_SECONDS)

    def wait(self):
        self._thread = Thread(target=self._handle_wait)
        self._thread.daemon = True
        self._watching = True
        self._thread.start()

    def clear(self):
        self._watching = False


GREEN_BTN = Button(name="GREEN_BTN", group="gphoto", pin=Pins.GREEN_BUTTON)

YELLOW_BTN = Button(name="YELLOW_BTN", group="gphoto", pin=Pins.YELLOW_BUTTON)

BLUE_BTN = Button(name="BLUE_BTN", group="gphoto", pin=Pins.BLUE_BUTTON)

RED_BTN = Button(name="RED_BTN", group="gphoto", pin=Pins.RED_BUTTON)

LEFT_BUTTON = Button(name="LEFT_BTN", group="gphoto", pin=Pins.LEFT_BUTTON)

RIGHT_BUTTON = Button(name="RIGHT_BTN", group="gphoto", pin=Pins.RIGHT_BUTTON)

RESET_BUTTON = Button(name="RESET_BTN", group="os", pin=Pins.RESET_BUTTON)


class Buttons:
    GREEN_BTN = GREEN_BTN
    YELLOW_BTN = YELLOW_BTN
    BLUE_BTN = BLUE_BTN
    RED_BTN = RED_BTN
    LEFT_BUTTON = LEFT_BUTTON
    RIGHT_BUTTON = RIGHT_BUTTON
    RESET_BUTTON = RESET_BUTTON


""""


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

"""
