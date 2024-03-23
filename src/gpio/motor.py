import gpiod
from gpiod.line import Direction, Value, Bias

# from . import MicroMotor, Pins

# VIBRATE_MOTOR = MicroMotor(
#     name="Error Status Indicator",
#     pin=Pins.MICRO_MOTOR_PIN,
#     settings=gpiod.LineSettings(
#         direction=Direction.OUTPUT,
#         output_value=Value.INACTIVE,
#         bias=Bias.PULL_DOWN,
#     ),
# )


# class VibratingMotors:
#     MAIN = VIBRATE_MOTOR
