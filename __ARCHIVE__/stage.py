from enum import Enum
from typing import List

from .logger import Logger
from .audio.audio import Sounds
from .play import play


class TimeUnit(Enum):
    SECONDS = 'SECONDS'
    MINUTES = 'MINUTES'


class TimeValue(Enum):
    SIXTY = 60
    THIRTY = 30
    TWENTY = 20
    TEN = 10
    NINE = 9
    EIGHT = 8
    SEVEN = 7
    SIX = 6
    FIVE = 5
    FOUR = 4
    THREE = 3
    TWO = 2
    ONE = 1


class Stage():
    log: Logger
    name: str
    tasks: List[dict]
    name_sound: Sounds
    countdown: bool = False

    # todo: alert_times only 30 or 30
    def __init__(
        self,
        name,
        name_sound: Sounds,
        tasks: List[dict]
    ):
        self.log = Logger(__name__)
        self.name = name
        self.name_sound = name_sound
        self.tasks = tasks

        self.log.info(f"Stage Created: {name}")

    def add_task(self, task):
        self.tasks = self.tasks + task

    def log_deets(self):
        self.log.json(self.name)
        self.log.json(self.name_sound)
        self.log.json(self.name_sound)
        self.log.json(self.tasks)

    def notify(self, val: TimeValue, unit: TimeUnit):
        self.log.info(
            f"{self.name} begins in {val.value} {unit.value}")

        play([self.name_sound, Sounds.BEGINS_IN,
             Sounds[f"{val.value}"], Sounds.SECONDS])

    def countdown(self):
        self.log.info(
            f"{self.name} begins in T-minus")

        sounds = [self.name_sound, Sounds.BEGINS_IN,
                  Sounds.T_MINUS]
        play(sounds)
