"""Titles, marks and expected texts of the eight lab tasks (the grader cannot import the instructor kit, so they are repeated here)."""
from __future__ import annotations

from typing import Dict, List

TITLES: Dict[int, str] = {
    1: "Read what is there", 2: "Write with echo", 3: "Edit with nano", 4: "Copy", 5: "Move and rename",
    6: "Delete", 7: "Search", 8: "Productivity and report",
}
MARKS: Dict[int, int] = {1: 14, 2: 12, 3: 12, 4: 12, 5: 10, 6: 14, 7: 16, 8: 10}

CLONE = "file-operations-lab"
RC = "robot-controller"

NOTES_FINAL: List[str] = ["# Lab notes", "Sensor threshold: 50 cm", "TODO: test with real hardware"]
SENSOR_PREFIX = "# sensor.py - "
SENSOR_FUNCTION: List[str] = ["def stop_distance(cm):", "return cm < 50"]
SUMMARY_PREFIX = "Summary: all files organised - "
PYC_PAIR = {"./sensor.pyc", "./src/motor/pwm.pyc"}
PYC_FILES = ("sensor.pyc", "src/motor/pwm.pyc")
