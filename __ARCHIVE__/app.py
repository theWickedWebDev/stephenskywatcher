from enum import Enum, auto
import sys
import schedule
from schedule import repeat, every
from typing import List
import time

from .logger import Logger as _Logger
from .stage import Stage, TimeValue, TimeUnit
from .audio.audio import Sounds
from .gphoto2 import gphoto
import datetime
from .play import play
from .config import get_times

Logger = _Logger(__name__)


@repeat(every().second)
def time_logger():
    Logger.time()


def notify(task, stage):
    stage.notify(val=task.get('time_val'), unit=task.get('time_unit'))


def countdown(task, stage):
    stage.countdown()


def sound(task, stage):
    Logger.info(task.get('sound').name)
    play([task.get('sound')])


def prepare_to_see(task, stage):
    Logger.info(f"Prepare to see {task.get('sound').name}")
    play([Sounds.PREPARE_TO_SEE, task.get('sound')])


def prepare_for(task, stage):
    Logger.info(f"Prepare for {task.get('sound').name}")
    play([Sounds.PREPARE_FOR, task.get('sound')])


def capture_partial(task, stage):
    Logger.info(f"Capturing partial eclipse")
    # gphoto()


def action(task, stage):
    Logger.debug(task.get('type'))
    if task.get('type') == 'NOTIFY':
        notify(task, stage)
    elif task.get('type') == 'COUNTDOWN':
        countdown(task, stage)
    elif task.get('type') == 'SOUND':
        sound(task, stage)
    elif task.get('type') == 'PREPARE_TO_SEE':
        prepare_to_see(task, stage)
    elif task.get('type') == 'PREPARE_FOR':
        prepare_for(task, stage)
    elif task.get('type') == 'CAPTURE_PARTIAL':
        capture_partial(task, stage)
    else:
        Logger.error('Unhandled task type')
        Logger.debug(task)


class Tags(Enum):
    DEFAULT = auto()
    CAPTURE = auto()
    VOICE = auto()
    START = auto()


def main(mode="development"):
    times = get_times('production' if mode == 'production' else 'development')

    def secondsBeforeStageStarts(stage, seconds):
        return times.get(stage) - datetime.timedelta(0, seconds+1)

    def final_countdown(stage):
        _steps = []
        # Fine Countdown
        for i in range(10):
            _steps.append({
                'type': 'SOUND',
                'time': secondsBeforeStageStarts(stage, i+1),
                "sound": Sounds[str(i+1)],
                'tag': Tags.VOICE
            })
        return _steps

    C1 = Stage(
        name='C1',
        name_sound=Sounds.C1,
        tasks=[
            {'type': 'NOTIFY', 'time': secondsBeforeStageStarts(
                'C1', 60), "time_val": TimeValue.SIXTY, "time_unit": TimeUnit.SECONDS, 'tag': Tags.VOICE},
            {'type': 'NOTIFY', 'time': secondsBeforeStageStarts(
                'C1', 30), "time_val": TimeValue.THIRTY, "time_unit": TimeUnit.SECONDS, 'tag': Tags.VOICE},
            {'type': 'NOTIFY', 'time': secondsBeforeStageStarts(
                'C1', 20), "time_val": TimeValue.TWENTY, "time_unit": TimeUnit.SECONDS, 'tag': Tags.VOICE},
            {'type': 'COUNTDOWN', 'time': secondsBeforeStageStarts(
                'C1', 13), 'tag': Tags.VOICE},
            {'type': 'SOUND', 'time': secondsBeforeStageStarts(
                'C1', 0), "sound": Sounds['FIRST_CONTACT'], 'tag': Tags.START},
            {'type': 'CAPTURE_PARTIAL', 'time': secondsBeforeStageStarts(
                'C1', 60), 'tag': Tags.CAPTURE},
        ]
    )

    Stages: List[Stage] = [C1]

    for stage in Stages:
        stage.add_task(final_countdown(stage.name))
        for task in stage.tasks:
            schedule.every().day.at(task.get('time').strftime(
                "%H:%M:%S")).do(action, task=task, stage=stage).tag(task.get('tag', Tags.DEFAULT).name)

    while True:
        schedule.run_pending()
        time.sleep(1)
        # time_of_next_run = schedule.next_run(Tags.START)
        # time_now = datetime.datetime.now()
        # time_remaining = time_of_next_run - time_now
        # Logger.remaining(time_remaining.seconds)


mode = sys.argv[1] if len(sys.argv) == 2 else 'development'

main(mode)
