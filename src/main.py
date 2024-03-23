import time
import sys
import gpiod
from filelock import FileLock
import schedule
import threading
from .gpio import Buttons, Leds, Speed, wait_for_button_press
from . import Functions

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

def main():
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

        f = Functions(gpio, Leds)
        Buttons.GREEN_BTN.onpress = lambda: f.bracketed()
        Buttons.YELLOW_BTN.onpress = lambda: f.continuous()
        Buttons.BLUE_BTN.onpress = lambda: f.manual_bracketed()
        Buttons.RED_BTN.onpress = lambda: f.manual_bracketed()
        Buttons.LEFT_BUTTON.onpress = lambda: f.download_latest()

        for b in BUTTONS:
            b.gpio = gpio
            b.thread = threading.Thread(target=wait_for_button_press, args=(b,BUTTONS,))
            b.thread.daemon = True
            b.thread.start()

        try:
            while True:
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


# mode = sys.argv[1] if len(sys.argv) == 2 else "development"
main()

"""
times = get_times("production" if mode == "production" else "development")
def test():
print('test')
display_image("/home/stephen/stephenskywatcher/eclipse.jpg")

now = datetime.datetime.now()
t = 8
jt = now + datetime.timedelta(0, t)
schedule.every().day.at(jt.strftime("%H:%M:%S")).do(test).tag("C1")
"""