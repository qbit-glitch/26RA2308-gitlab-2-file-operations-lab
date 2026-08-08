# plot.py - print a text bar for each reading
import math


def bar(value):
    return "#" * math.ceil(value * 10)
