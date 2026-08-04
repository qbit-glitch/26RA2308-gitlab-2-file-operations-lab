# pwm.py - pulse width helper for the motors
import time
import math


def duty_for_speed(speed):
    # TODO: add a soft start
    return math.floor(speed * 2.55)


def wait_ms(ms):
    time.sleep(ms / 1000)
