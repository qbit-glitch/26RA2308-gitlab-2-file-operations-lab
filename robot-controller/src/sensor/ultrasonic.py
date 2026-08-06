# ultrasonic.py - range reader for the front sensor
import time
import statistics


def read_cm(echo_ms):
    # TODO: reject outliers
    return echo_ms * 17


def settle():
    time.sleep(0.05)
