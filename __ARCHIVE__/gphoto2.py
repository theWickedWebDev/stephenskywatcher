import os
import subprocess
from threading import Thread

from .logger import Logger as _Logger

Logger = _Logger(__name__)

FILENAME = "/home/stephen/Documents/eclipse-py/captures/%m-%d-%y_%H:%M:%S-%f.%C"
IMAGEFORMAT = 7  # raw:7  both:6
FRAMES = 1
FOCAL = 55
ISO = 800
APERTURE = 9  # 5.6
EXPOSURE = 3  # Exposure, in seconds
AUTOEXPOSUREMODE = 3  # manual
PICTURESTYLE = 2  # landscape
HISTOGRAM = 0
SHUTTERSPEED = "1/4000"
DRIVEMODE = 1  # coninuous:1 single:0
AEB = 0  # Current: offChoice: 0 off Choice: 1 +/- 1/3 Choice: 2 +/- 2/3 Choice: 3 +/- 1 Choice: 4 +/- 1 1/3 Choice: 5 +/- 1 2/3 Choice: 6 +/- 2
CAPTURETARGET = 1  # ram:0  card:1
FRAMES = 3  # 5.6

# SHUTTER_EXPOSURE = f"""gphoto2 \
#     --set-config imageformat={IMAGEFORMAT} \
#     --set-config picturestyle={PICTURESTYLE} \
#     --set-config autoexposuremode={AUTOEXPOSUREMODE} \
#     --set-config aperture={APERTURE} \
#     --set-config shutterspeed="{SHUTTERSPEED}" \
#     --set-config drivemode="{DRIVEMODE}" \
#     --set-config iso={ISO} \
#     --set-config aeb={AEB} \
#     --no-keep \
#     --filename {FILENAME} \
#     --frames {FRAMES} \
#     --capture-image-and-download"""

# CAPTURE_INTERVAL = f"""gphoto2 \
#     --filename {FILENAME} \
#     --force-overwrite \
#     --capture-image
#     """

CAPTURE_CONTINUOUS = f"""gphoto2 \
    --set-config drivemode=1 \
    --set-config aeb=0 \
    --filename {FILENAME} \
    --set-config eosremoterelease=2 \
    --wait-event=5s \
    --set-config eosremoterelease=11
    """

DOWNLOAD_ALL = F"""gphoto2 \
    --new \
    --filename {FILENAME} \
    --force-overwrite \
    --get-all-files
    """


def _capture():
    CONFIG = f"""gphoto2 \
    --set-config drivemode="{DRIVEMODE}" \
    --set-config imageformat={IMAGEFORMAT} \
    --set-config picturestyle={PICTURESTYLE} \
    --set-config aeb={AEB} \
    --set-config autoexposuremode={AUTOEXPOSUREMODE} \
    --set-config aperture={APERTURE} \
    --set-config shutterspeed="{SHUTTERSPEED}" \
    --set-config focusmode=0 \
    --set-config iso={ISO} \
    --set-config capturetarget="{CAPTURETARGET}" \
    """

    subprocess.run(CONFIG, shell=True, capture_output=True)

    result = subprocess.run(CAPTURE_CONTINUOUS, shell=True,
                            capture_output=True, universal_newlines=True, text=True)
    if result.stdout:
        Logger.debug(result.stdout)
    if result.stderr:
        Logger.error(result.stderr)

    result = subprocess.run(DOWNLOAD_ALL, shell=True, capture_output=True)


def gphoto():
    Thread(target=_capture).start()
