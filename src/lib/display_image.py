import threading
from sh import eog


def display_image(path: str):
    eog(["--fullscreen", path])
