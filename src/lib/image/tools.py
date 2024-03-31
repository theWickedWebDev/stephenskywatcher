import os
import glob
from pathlib import Path
import rawpy
import imageio
import os
import threading
from sh import eog


def _display(path):
    eog(
        [
            "--fullscreen",
            path,
        ]
    )


def display_image(path: str):
    t = threading.Thread(target=_display, args=(path,))
    t.daemon = True
    t.start()


def convert_raw_to_jpg(img):
    new_file_path = Path(img).parent.resolve()
    new_file = Path(img).stem

    with rawpy.imread(img) as raw:
        rgb = raw.postprocess(rawpy.Params(use_camera_wb=True))
        new_location = f"{new_file_path}/{new_file}.jpg"
        imageio.imsave(new_location, rgb)
        return new_location


def get_latest_file(path, *paths):
    """Returns the name of the latest (most recent) file
    of the joined path(s)"""
    fullpath = os.path.join(path, *paths)
    list_of_files = glob.glob(fullpath)  # You may use iglob in Python3
    if not list_of_files:  # I prefer using the negation
        return None  # because it behaves like a shortcut
    latest_file = max(list_of_files, key=os.path.getctime)
    _, filename = os.path.split(latest_file)
    return filename


def display_latest_file(path: Path, pattern: str = "*"):
    latest_file = get_latest_file(f"{path}/*")
    full_path_latest_file = f"{path}/{latest_file}"
    if "CR3" in full_path_latest_file:
        new_image = convert_raw_to_jpg(full_path_latest_file)
        display_image(new_image)
    else:
        display_image(full_path_latest_file)
