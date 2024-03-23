import time
import datetime
import sys
import gpiod
from filelock import FileLock
import schedule
from schedule import repeat, every
import threading
from .audio.audio import Sounds
from .config import get_times
from .lib import play, display_image
from .gpio import Button, Buttons, Leds, Speed
from . import (
    capture_bracketed,
    capture_continuous,
    capture_manual_bracketed,
)

"""
Example Base Setting choices:
f/8 ISO200
f/11 ISO100
f/12.6 ISO200
"""

"""
Pre Eclipse
  - Simple exposure on a long interval
    * Need to be able to +/- exposure

Partial Eclipse
  - Simple exposure on a long interval
    * Need to be able to +/- exposure

Baily's Beads (~30s before Totality)
  - Fast as I can bracketed exposures

Totality (4min 21sec)
    - Bracketed exposures
    * Slowly ramp up exposure to full corona shot at max totality
    ** Ramp values:
        - Start: 1/4000
        - End: [max totality exposure]

    == Buttons
        -Start Totality Button, ramps up shots [0:00 to 2:00]

    
MAX Totality (~40s)
    - 1 long exposure (8s 12s?) to capture Earthshine on Moon
    * Slowly ramp down exposure until Baily's beads (C3)
    ** Ramp values:
        - Start: [max totality exposure]
        - End: 1/4000
    
    == Buttons
        -Start Max Button, takes 5 exposures:
          5s  > 0:00-0:05
          7s  > 0:06-0:13
          10s > 0:14-0:24
          7s  > 0:25-0:32
          5s  > 0:33-0:38

Baily's Beads: [repeat above]
Partial Eclipse: [repeat above]
Post Exclipse: [repeat above]

*Gotcha* - Need a time either before or after max totality for a picture of people
          - probably needs to be a slightly longish exposure
"""

"""
TIMING: 4m21s (total)

(21s)
First Baily's Beads: -20s + (10s of totality)
Second Baily's Beads: (10s of totality) + 10s

Remaining for Totality: 4m

-----
-0:20: Baily's start
 #
 0:00: (Totality start)
 0:10: Baily's end
 #
 0:12: Ramp up start      (+10s start)
 1:42: Ramp up end        (-18s max)
 #
 1:44: Max Totality Start (-16s max)
 2:00: (Max Totality)
 2:16: Max Totality End   (+16s max)
 #
 2:18: Ramp down start    (+18s max)
 0:00: Ramp down end      (-10s start)
 #
+0:20: Baily's ends
"""

from .logger import Logger as _Logger

Logger = _Logger(__name__)

LOCK_FILE = "/home/stephen/stephenskywatcher/startup.lock"
POLL_INTERVAL = 0.05

LEDS = [Leds.YELLOW_LED, Leds.GREEN_LED, Leds.RED_LED]
BUTTONS = [
    Buttons.GREEN_BTN,
    Buttons.YELLOW_BTN,
    Buttons.BLUE_BTN,
    Buttons.RED_BTN,
    Buttons.LEFT_BUTTON,
    Buttons.RIGHT_BUTTON,
    Buttons.RESET_BUTTON,
]

GPIO_CONFIG = {}
for b in BUTTONS + LEDS:
    GPIO_CONFIG.update({b.pin: b.settings})

# TODO: BUTTON: Download latest photo and display
# TODO: BUTTON: + / - Exposure
# TODO: BUTTON: complete reset
#       - ps aux | grep gphoto2 (and kill)
#        - perhaps gpio lock?
# TODO: LCD: Add stats to character display, ie countdown, captures, current camera settings? (i2c)


def gpio_off(gpio):
    Leds.GREEN_LED.turn_off(gpio)
    Leds.RED_LED.turn_off(gpio)
    Leds.YELLOW_LED.turn_off(gpio)


def startup(gpio):

    Leds.RED_LED.flicker(gpio, Speed.FAST)
    time.sleep(0.4)
    Leds.RED_LED.stop_flicker()

    Leds.YELLOW_LED.flicker(gpio, Speed.FAST)
    time.sleep(0.4)
    Leds.YELLOW_LED.stop_flicker()

    Leds.GREEN_LED.flicker(gpio, Speed.FAST)
    time.sleep(0.4)
    Leds.GREEN_LED.stop_flicker()

    Leds.GREEN_LED.turn_on(gpio)
    Leds.YELLOW_LED.turn_off(gpio)
    Leds.RED_LED.turn_off(gpio)


def wait_for_button_press(btn: Button):
    while True:
        if not btn.press_event.is_set() and btn.is_pressed():
            print(btn.name)

            group_busy = False
            for b in BUTTONS:
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
        time.sleep(POLL_INTERVAL)


def main(mode):
    times = get_times("production" if mode == "production" else "development")

    def test():
        display_image("/home/stephen/stephenskywatcher/eclipse.jpg")
        # play([Sounds.WELCOME_ECLIPSE])

    # play(
    #     [
    #         Sounds.TOTALITY,
    #         Sounds.BEGINS_IN,
    #         Sounds.T_MINUS,
    #         Sounds.TEN,
    #         Sounds.SECONDS,
    #         Sounds.COUNTDOWN_AMELIA,
    #     ]
    # )
    #

    now = datetime.datetime.now()
    t = 8
    jt = now + datetime.timedelta(0, t)
    print(jt)
    schedule.every().day.at(jt.strftime("%H:%M:%S")).do(test).tag("C1")

    with (
        FileLock(LOCK_FILE) as Lock,
        gpiod.request_lines(
            "/dev/gpiochip4",
            consumer="capture",
            config=GPIO_CONFIG,
        ) as gpio,
    ):
        startup(gpio)
        gpio_off(gpio)

        def test2():
            VibratingMotors.MAIN.flicker(gpio, Speed.VERY_FAST)
            time.sleep(0.5)
            VibratingMotors.MAIN.turn_off(gpio)

        Buttons.GREEN_BTN.onpress = lambda: capture_bracketed(
            Leds, gpio
        )  # capture_bracketed,
        Buttons.YELLOW_BTN.onpress = lambda: capture_continuous(
            Leds, gpio
        )  # capture_bracketed,
        Buttons.BLUE_BTN.onpress = lambda: capture_manual_bracketed(
            Leds, gpio
        )  # capture_bracketed,
        Buttons.RED_BTN.onpress = lambda: capture_bracketed(Leds, gpio)
        #
        Buttons.LEFT_BUTTON.onpress = test2
        # TODO: There must be a better built-in gpiod way
        #       to handle this, instead of a single thread for each?
        #       - if so, is it worth it?
        for b in BUTTONS:
            b.gpio = gpio
            b.thread = threading.Thread(target=wait_for_button_press, args=(b,))
            b.thread.daemon = True
            b.thread.start()

        try:
            while True:
                # How can I not have this....
                # TODO: Scheduler: print current time, next event countdown, etc...

                schedule.run_pending()
                time.sleep(1)
        except KeyboardInterrupt:
            gpio_off(gpio)
            pass
        except Exception as e:
            Logger.error(e)
            pass
        finally:
            gpio_off(gpio)
            Lock.release()
            gpio.release()
            Logger.warning("goodbye")


mode = sys.argv[1] if len(sys.argv) == 2 else "development"

main(mode)
