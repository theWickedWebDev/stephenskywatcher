from typing import List
import time
import gpiod
from filelock import FileLock
from .lib import Button, Buttons, Led, Leds
from .functions import reset_all, Functions
from .lib.logger import Logger as _Logger
from .lib import Camera as _Camera, Shoot as _Shoot, Hooks as _Hooks, killgphoto2Process

Logger = _Logger(__name__)

LOCK_FILE = "/home/stephen/stephenskywatcher/startup.lock"

BUTTONS: List[Button] = [
    Buttons.GREEN_BTN,
    Buttons.YELLOW_BTN,
    Buttons.BLUE_BTN,
    Buttons.RED_BTN,
    Buttons.LEFT_BUTTON,
    Buttons.RIGHT_BUTTON,
    Buttons.RESET_BUTTON,
]

LEDS: List[Led] = [Leds.GREEN_LED, Leds.RED_LED, Leds.YELLOW_LED]

GPIO_CONFIG = {}
for g in BUTTONS + LEDS:
    GPIO_CONFIG.update({g.pin: g.line_settings})


def main(gpio):
    from .welcome import welcome

    welcome()

    for b in BUTTONS + LEDS:
        b.gpio = gpio

    f = Functions(gpio, Leds)

    # Exposure Adjustments
    Buttons.GREEN_BTN.on_long_press = f.prev_iso
    Buttons.YELLOW_BTN.on_long_press = f.next_iso
    Buttons.BLUE_BTN.on_long_press = f.prev_aperture
    Buttons.RED_BTN.on_long_press = f.next_aperture
    Buttons.RIGHT_BUTTON.on_long_press = f.prev_shutterspeed
    Buttons.LEFT_BUTTON.on_long_press = f.next_shutterspeed

    # Captures
    Buttons.GREEN_BTN.on_press = f.bracketed
    Buttons.YELLOW_BTN.on_press = f.continuous
    Buttons.BLUE_BTN.on_press = f.manual_bracketed
    Buttons.RED_BTN.on_press = f.capture
    Buttons.RIGHT_BUTTON.on_press = lambda: print("RIGHT_BUTTON PRESS")
    Buttons.LEFT_BUTTON.on_press = lambda: print("LEFT_BUTTON PRESS")

    # OS
    Buttons.RESET_BUTTON.on_long_press = reset_all
    Buttons.RESET_BUTTON.on_press = f.download_latest

    for b in BUTTONS:
        b.wait()

    Leds.GREEN_LED.on()

    while True:
        time.sleep(7)


def gpio_exit():
    for b in BUTTONS:
        b.press_event.clear()
    for l in LEDS:
        l.stop_flicker()


killgphoto2Process()
with (
    FileLock(LOCK_FILE, thread_local=False) as Lock,
    gpiod.request_lines(
        "/dev/gpiochip4",
        consumer="capture",
        config=GPIO_CONFIG,
    ) as gpio,
):
    main(gpio)
