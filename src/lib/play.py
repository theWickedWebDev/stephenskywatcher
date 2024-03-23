import os
from threading import Thread


def play(sounds):
    def _play():
        for sound in sounds:
            os.system(f"ffplay {sound.value} -nodisp -nostats -hide_banner -autoexit")

    Thread(target=_play).start()


def play_sync(sounds):
    for sound in sounds:
        os.system(f"ffplay {sound.value} -nodisp -nostats -hide_banner -autoexit")
