from contextlib import contextmanager
import logging
import locale
import time
import os
import subprocess
import sys
import gphoto2 as gp

INTERVAL = 10.0
WORK_DIR = '/tmp/time_lapse'
OUT_FILE = 'time_lapse.mp4'

@contextmanager
def configured_camera():
    # initialise camera
    camera = gp.Camera()
    camera.init()
    try:
        # adjust camera configuratiuon
        cfg = camera.get_config()
        capturetarget_cfg = cfg.get_child_by_name('capturetarget')
        capturetarget = capturetarget_cfg.get_value()
        capturetarget_cfg.set_value('Internal RAM')
        # camera dependent - 'imageformat' is 'imagequality' on some
        imageformat_cfg = cfg.get_child_by_name('imageformat')
        imageformat = imageformat_cfg.get_value()
        imageformat_cfg.set_value('Small Fine JPEG')
        camera.set_config(cfg)
        # use camera
        yield camera
    finally:
        # reset configuration
        capturetarget_cfg.set_value(capturetarget)
        imageformat_cfg.set_value(imageformat)
        camera.set_config(cfg)
        # free camera
        camera.exit()


def empty_event_queue(camera):
    while True:
        type_, data = camera.wait_for_event(10)
        if type_ == gp.GP_EVENT_TIMEOUT:
            return
        if type_ == gp.GP_EVENT_FILE_ADDED:
            # get a second image if camera is set to raw + jpeg
            print('Unexpected new file', data.folder + data.name)


def main():
    locale.setlocale(locale.LC_ALL, '')
    if not os.path.exists(WORK_DIR):
        os.makedirs(WORK_DIR)
    template = os.path.join(WORK_DIR, 'frame%04d.jpg')
    next_shot = time.time() + 1.0
    count = 0
    with configured_camera() as camera:
        while True:
            try:
                empty_event_queue(camera)
                while True:
                    sleep = next_shot - time.time()
                    if sleep < 0.0:
                        break
                    time.sleep(sleep)
                path = camera.capture(gp.GP_CAPTURE_IMAGE)
                print('capture', path.folder + path.name)
                camera_file = camera.file_get(
                    path.folder, path.name, gp.GP_FILE_TYPE_NORMAL)
                camera_file.save(template % count)
                camera.file_delete(path.folder, path.name)
                next_shot += INTERVAL
                count += 1
            except KeyboardInterrupt:
                break

    subprocess.check_call(['ffmpeg', '-r', '25', '-i', template, '-c:v', 'h264', OUT_FILE])
    for i in range(count):
        os.unlink(template % i)
    return 0


if __name__ == "__main__":
    sys.exit(main())