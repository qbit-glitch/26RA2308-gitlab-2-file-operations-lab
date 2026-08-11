"""Graders for lab tasks 1 to 4 (14 + 12 + 12 + 12 = 50 marks)."""
from __future__ import annotations

import os
from typing import Optional

from . import lsparse, published
from .context import Ctx
from .framework import Task
from .listing import (OTHER_FILE_NAMES, block, children, has_name, named_rows, names, rows_show, student_name,
                      top_level, PUBLISHED_NAMES)
from .taskinfo import CLONE, MARKS, NOTES_FINAL, RC, SENSOR_FUNCTION, SENSOR_PREFIX, TITLES

LOG = published.FILES["mission_log.txt"].split("\n")[:-1]
OLD_NOTES = published.FILES["notes.txt"].split("\n")[:-1]
FACTS = published.FACTS


def grade_task1(ctx: Ctx) -> Task:
    """Read what is there: pwd, cat, head and tail -5 of the mission log."""
    task = Task(1, TITLES[1], MARKS[1], ctx.repo_mode)
    pasted = lsparse.paths(ctx.step("1.1"))
    task.check(2, "1.1 pwd ends in /file-operations-lab/robot-controller",
               lsparse.path_ends(ctx.step("1.1"), f"{CLONE}/{RC}"))
    task.check(3, "1.2 cat prints every line of mission_log.txt", block(ctx, "1.2", LOG))
    task.check(2, "1.3 head prints the first 10 lines of mission_log.txt", block(ctx, "1.3", LOG[:10]))
    task.check(2, "1.4 tail -5 prints the last 5 lines of mission_log.txt", block(ctx, "1.4", LOG[-5:]))
    task.check(1, "ANSWER-1 is the number of lines head left out",
               lsparse.answer_number(ctx.text, 1) == FACTS["head_missing"])
    task.check(1, "ANSWER-2 is the time of the last entry", lsparse.answer_is(ctx.text, 2, FACTS["last_entry_time"]))
    task.check(1, "the Name line of outputs.txt is filled in", bool(student_name(ctx)))
    task.check(2, "the pwd you pasted in 1.1 is this clone",
               lambda: os.name == "nt" or (bool(pasted) and ctx.facts.is_this_clone(pasted[0])), needs_repo=True)
    return task


def grade_task2(ctx: Ctx) -> Task:
    """Write with echo: > overwrites, >> appends."""
    task = Task(2, TITLES[2], MARKS[2], ctx.repo_mode)
    task.check(2, "2.1 cat shows the old lines of notes.txt", block(ctx, "2.1", OLD_NOTES))
    task.check(2, "2.2 after > notes.txt holds only the first new line", block(ctx, "2.2", NOTES_FINAL[:1]))
    task.check(1, "2.3 after the first >> notes.txt holds two lines", block(ctx, "2.3", NOTES_FINAL[:2]))
    task.check(2, "2.4 after the second >> notes.txt holds the three lines", block(ctx, "2.4", NOTES_FINAL))
    task.check(1, "ANSWER-3 is the number of old lines that > destroyed",
               lsparse.answer_number(ctx.text, 3) == FACTS["old_notes_lines"])
    task.check(4, "notes.txt in your folder holds exactly the three lines",
               lambda: ctx.facts.lines("notes.txt") == NOTES_FINAL, needs_repo=True)
    return task


def _sensor_size(ctx: Ctx) -> Optional[int]:
    """The size of sensor.py the 3.2 listing shows, if it is a plausible one (the real one when there is a clone)."""
    row = named_rows(ctx.step("3.2")).get("sensor.py")
    if row is None or row.kind != "-" or row.size <= 0:
        return None
    if ctx.repo_mode:
        return row.size if ctx.facts.size("sensor.py") == row.size else None
    return row.size


def _has_function(ctx: Ctx) -> bool:
    lines = ctx.facts.lines("sensor.py") or []
    first, second = SENSOR_FUNCTION
    return first in lines and second in lines[lines.index(first):]


def grade_task3(ctx: Ctx) -> Task:
    """Edit with nano: a signed function in sensor.py."""
    task = Task(3, TITLES[3], MARKS[3], ctx.repo_mode)
    name = student_name(ctx)
    size = _sensor_size(ctx)
    number = lsparse.answer_number(ctx.text, 4)
    task.check(3, "3.1 cat shows the signed first line and the function",
               bool(name) and block(ctx, "3.1", [SENSOR_PREFIX + name] + SENSOR_FUNCTION))
    task.check(2, "3.2 ls -l shows sensor.py as a file with its real size", size is not None)
    task.check(2, "ANSWER-4 is the size of sensor.py in the 3.2 listing", size is not None and number == size)
    task.check(3, "sensor.py in your folder holds the function you typed", lambda: _has_function(ctx), needs_repo=True)
    task.check(2, "sensor.py in your folder carries your name", lambda: has_name(ctx, ctx.facts.lines("sensor.py")),
               needs_repo=True)
    return task


def grade_task4(ctx: Ctx) -> Task:
    """Copy: a file and a folder."""
    task = Task(4, TITLES[4], MARKS[4], ctx.repo_mode)
    rows = named_rows(ctx.step("4.1"))
    original, copy = rows.get("sensor.py"), rows.get("sensor_backup.py")
    same = original is not None and copy is not None and original.kind == "-" == copy.kind and original.size == copy.size
    visible = PUBLISHED_NAMES
    task.check(3, "4.1 sensor_backup.py is listed as a file of the same size as sensor.py", same)
    # the size of sensor.py at the time of the copy: its real size, or the size of the empty file the lab gave
    # (a student who edits sensor.py in Task 3 only after copying it)
    task.check(2, "the sizes you pasted in 4.1 are the size your sensor.py had when you copied it",
               lambda: same and copy is not None and copy.size in (ctx.facts.size("sensor.py"), len(published.FILES["sensor.py"])),
               needs_repo=True)
    task.check(2, "4.1 the long listing shows the other files and folders of robot-controller",
               rows_show(ctx.step("4.1"), top_level("-"), top_level("d")))
    task.check(2, "4.2 ls shows src and its copy src_backup",
               names(ctx.step("4.2")) in (visible | {"src_backup", "sensor_backup.py"}, visible | {"src_backup"}))
    task.check(3, "4.3 the copy holds the same files as src/motor", names(ctx.step("4.3")) == children("src/motor"))
    return task
