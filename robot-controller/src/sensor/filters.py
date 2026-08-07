# filters.py - smoothing filters for sensor readings
import math
import statistics
import collections


def average(values):
    return statistics.mean(values)


def window(size):
    return collections.deque(maxlen=size)


def rms(values):
    return math.sqrt(sum(v * v for v in values) / len(values))
