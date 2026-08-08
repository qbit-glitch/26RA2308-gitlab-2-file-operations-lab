# calibrate.py - read and apply the motor offsets
import json
import sys


def load(path):
    # TODO: report a missing file
    with open(path) as handle:
        return json.load(handle)


if __name__ == "__main__":
    print(load(sys.argv[1]))
