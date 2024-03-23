import sys
import schedule
from schedule import repeat, every
from typing import List
import time

from .logger import Logger as _Logger
from .stage import Stage, TimeValue, TimeUnit
from .audio.audio import Sounds
import datetime
from .play import play
from .config import get_times

Logger = _Logger(__name__)


@repeat(every().second)
def time_logger():
    Logger.time()


def action(step, stage):
    if step.get('type') == 'NOTIFY':
        stage.notify(val=step.get('time_val'), unit=step.get('time_unit'))
    elif step.get('type') == 'COUNTDOWN':
        stage.countdown()
    elif step.get('type') == 'SOUND':
        Logger.info(step.get('sound').name)
        play([step.get('sound')])
    elif step.get('type') == 'PREPARE_TO_SEE':
        Logger.info(f"Prepare to see {step.get('sound').name}")
        play([Sounds.PREPARE_TO_SEE, step.get('sound')])
    elif step.get('type') == 'PREPARE_FOR':
        Logger.info(f"Prepare for {step.get('sound').name}")
        play([Sounds.PREPARE_FOR, step.get('sound')])


def main(mode="development"):
    times = get_times('production' if mode == 'production' else 'development')

    def secondsBeforeStageStarts(stage, seconds):
        return times.get(stage) - datetime.timedelta(0, seconds+1)

    def get_steps(stage):

        def n_second_warning(t, m, stage_name):
            return {'type': 'NOTIFY', 'time': times.get(stage_name) - datetime.timedelta(0, m), "time_val": t, "time_unit": TimeUnit.SECONDS, 'tag': 'WARNING'}

        def get_welcome_sound():
            if (stage == 'C1'):
                return Sounds['FIRST_CONTACT']
            if (stage == 'C2'):
                return Sounds['TOTALITY']
            if (stage == 'C3'):
                return Sounds['THIRD_CONTACT']
            if (stage == 'C4'):
                return Sounds['FOURTH_CONTACT']

        # Coarse Countdown
        _steps = [
            n_second_warning(TimeValue.SIXTY, 60, stage),
            n_second_warning(TimeValue.THIRTY, 30, stage),
            n_second_warning(TimeValue.TWENTY, 20, stage),
            {
                'type': 'SOUND',
                'time': secondsBeforeStageStarts(stage, 0),
                "sound": get_welcome_sound(),
                'tag': 'START'
            },
            {
                'type': 'COUNTDOWN',
                'time': secondsBeforeStageStarts(stage, 13),
                'tag': 'WARNING'
            },
        ]

        # Fine Countdown
        for i in range(10):
            _steps.append({
                'type': 'SOUND',
                'time': secondsBeforeStageStarts(stage, i+1),
                "sound": Sounds[str(i+1)],
                'tag': 'WARNING'
            })

        return _steps

    C1 = Stage(
        name='C1',
        name_sound=Sounds.C1,
        times=get_steps('C1') + [
            {
                'type': 'SOUND',
                'time': secondsBeforeStageStarts('C1', 25),
                "sound": Sounds['GLASSES_ON'],
                'tag': 'TASK'
            }
        ]
    )

    C2 = Stage(
        name='C2',
        name_sound=Sounds.C2,
        times=get_steps('C2') + [
            {
                'type': 'SOUND',
                'time': secondsBeforeStageStarts('C2', -2),
                "sound": Sounds.GLASSES_OFF,
                'tag': 'WARNING'
            }, {
                'type': 'PREPARE_TO_SEE',
                'time': secondsBeforeStageStarts('C2', 110),
                "sound": Sounds.BAILYS_BEADS,
                'tag': 'WARNING'
            }, {
                'type': 'PREPARE_TO',
                'time': secondsBeforeStageStarts('C2', 140),
                "sound": Sounds.REMOVE_SOLAR_FILTER,
                'tag': 'WARNING'
            }, {
                'type': 'SOUND',
                'time': secondsBeforeStageStarts('C2', 130),
                "sound": Sounds.REMOVE_SOLAR_FILTER,
                'tag': 'WARNING'
            },
        ]
    )

    C3 = Stage(
        name='C3',
        name_sound=Sounds.C3,
        times=get_steps('C3') + [
            {
                'type': 'SOUND',
                'time': secondsBeforeStageStarts('C3', 40),
                "sound": Sounds.GLASSES_ON,
                'tag': 'WARNING'
            }, {
                'type': 'PREPARE_TO_SEE',
                'time': secondsBeforeStageStarts('C3', 110),
                "sound": Sounds.BAILYS_BEADS,
                'tag': 'WARNING'
            }
        ]
    )

    C4 = Stage(
        name='C4',
        name_sound=Sounds.C4,
        times=get_steps('C4')
    )

    Stages: List[Stage] = [C1, C2, C3, C4]

    Logger.json(C1.times)
    MANUAL_TASKS = [{
        'type': 'SOUND',
        'time': datetime.datetime.now() + datetime.timedelta(0, 3),
        "sound": Sounds['ATTACH_SOLAR_FILTER'],
        'tag': 'TASK'
    }]

    for stage in Stages:
        for step in stage.times:
            schedule.every().day.at(step.get('time').strftime(
                "%H:%M:%S")).do(action, step=step, stage=stage).tag(step.get('tag', 'NONE'))

    for task in MANUAL_TASKS:
        schedule.every().day.at(task.get('time').strftime(
            "%H:%M:%S")).do(action, step=task, stage=None).tag(step.get('tag', 'NONE'))

    while True:
        schedule.run_pending()
        time.sleep(1)
        time_of_next_run = schedule.next_run('START')
        time_now = datetime.datetime.now()
        time_remaining = time_of_next_run - time_now
        Logger.remaining(time_remaining.seconds)


mode = sys.argv[1] if len(sys.argv) == 2 else 'development'

main(mode)
