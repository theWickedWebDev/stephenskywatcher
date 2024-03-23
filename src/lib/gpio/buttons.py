from threading import Thread
from gpiod import LineSettings
from gpiod.line import Direction, Edge

from ...logger import Logger as _Logger
from .gpio import Gpio, Pin, Pins

Logger = _Logger(__name__)

class Button(Gpio):
    def __init__(self,
                 name: str,
                 group: str,
                 pin: Pin,
                 direction: Direction = Direction.INPUT,
                 edge_detection: Edge = Edge.FALLING,
    ):
        self.name = name
        self.group = group
        self.pin = pin
        self.logger = _Logger('Button')
        self.on_press = None
        self._thread: Thread = Thread(target=self._on_change)
        self.line_settings = LineSettings(
            direction=direction,
            edge_detection=edge_detection,
        )
    
    def _on_change(self):
        print('asdf')

GREEN_BTN = Button(
    name="GREEN_BTN",
    group="gphoto",
    pin=Pins.GREEN_BUTTON
)

YELLOW_BTN = Button(
    name="YELLOW_BTN",
    group="gphoto",
    pin=Pins.YELLOW_BUTTON
)

BLUE_BTN = Button(
    name="BLUE_BTN",
    group="gphoto",
    pin=Pins.BLUE_BUTTON
)

RED_BTN = Button(
    name="RED_BTN",
    group="gphoto",
    pin=Pins.RED_BUTTON
)

LEFT_BUTTON = Button(
    name="LEFT_BTN",
    group="gphoto",
    pin=Pins.LEFT_BUTTON
)

RIGHT_BUTTON = Button(
    name="RIGHT_BTN",
    group="gphoto",
    pin=Pins.RIGHT_BUTTON
)

RESET_BUTTON = Button(
    name="RESET_BTN",
    group="os",
    pin=Pins.RESET_BUTTON
)


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