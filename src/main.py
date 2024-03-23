from typing import List
import time
import gpiod
from filelock import FileLock

from .logger import Logger as _Logger
from .lib import Button, Buttons

Logger = _Logger(__name__)

BUTTONS: List[Button] = [
    Buttons.GREEN_BTN,
    Buttons.YELLOW_BTN,
    Buttons.BLUE_BTN,
    Buttons.RED_BTN,
    Buttons.LEFT_BUTTON,
    Buttons.RIGHT_BUTTON,
    Buttons.RESET_BUTTON,
]

GPIO_CONFIG = {}
for b in BUTTONS:
    GPIO_CONFIG.update({b.pin: b.line_settings})

def main(gpio):
    Buttons.GREEN_BTN.on_press = lambda: print('green btn')
    Buttons.YELLOW_BTN.on_press = lambda: print('yellow btn')
    Buttons.BLUE_BTN.on_press = lambda: print('blue btn')
    Buttons.RED_BTN.on_press = lambda: print('red btn')
    Buttons.LEFT_BUTTON.on_press = lambda: print('left btn')
    Buttons.RIGHT_BUTTON.on_press = lambda: print('right btn')

    while True:
        # TODO: Scheduler: print current time, next event countdown, etc...
        # schedule.run_pending()
        time.sleep(1)


try:
    LOCK_FILE = "/home/stephen/stephenskywatcher/startup.lock"
    with (
        FileLock(LOCK_FILE) as Lock,
        gpiod.request_lines(
            "/dev/gpiochip4",
            consumer="capture",
            config=GPIO_CONFIG,
        ) as gpio,
    ):
        main(gpio)

except KeyboardInterrupt:
    Lock.release()
    gpio.release()
    pass
except Exception as e:
    Logger.error(e)
    Lock.release()
    gpio.release()
    pass
finally:
    Lock.release()
    gpio.release()
    Logger.warning("goodbye")