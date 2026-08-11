"""Graders for lab tasks 5 to 8 (10 + 14 + 16 + 10 = 50 marks)."""
from __future__ import annotations

import os
from typing import Optional

from . import content, lsparse, published
from .context import Ctx
from .framework import Task
from .listing import (PUBLISHED_NAMES, answer_only, block, children, find_sets, grep_sets, has_name, names,
                      student_name, named_rows)
from .taskinfo import MARKS, PYC_PAIR, SUMMARY_PREFIX, TITLES

LOG = published.FILES["mission_log.txt"].split("\n")[:-1]
FACTS = published.FACTS


def grade_task5(ctx: Ctx) -> Task:
    """Move and rename: mv renames, mkdir makes a folder, mv puts a file into it."""
    task = Task(5, TITLES[5], MARKS[5], ctx.repo_mode)
    after_mv, after_move = names(ctx.step("5.1")), names(ctx.step("5.3"))
    task.check(3, "5.1 ls shows sensor_old.py and no sensor_backup.py",
               "sensor_old.py" in after_mv and "sensor_backup.py" not in after_mv)
    task.check(2, "5.1 ls still shows the other files of the folder", PUBLISHED_NAMES <= after_mv)
    task.check(3, "5.2 ls archive/ shows only sensor_old.py", names(ctx.step("5.2")) == {"sensor_old.py"})
    task.check(2, "5.3 ls shows archive and neither sensor_old.py nor sensor_backup.py",
               PUBLISHED_NAMES <= after_move and "archive" in after_move
               and not ({"sensor_old.py", "sensor_backup.py"} & after_move))
    return task


def _intact(ctx: Ctx, wanted: "set[str]") -> bool:
    """Every published file whose path starts with one of 'wanted' is there with its published text."""
    return all(ctx.facts.read(path) == text for path, text in published.FILES.items()
               if path.split("/")[0] in wanted or path in wanted)


def grade_task6(ctx: Ctx) -> Task:
    """Delete: rm, rm -r and rm -i."""
    task = Task(6, TITLES[6], MARKS[6], ctx.repo_mode)
    rows61 = named_rows(ctx.step("6.1"))
    after = {n: names(ctx.step(n)) for n in ("6.2", "6.4")}
    after63 = names(ctx.step("6.3"))
    asked = any("?" in line and "old_motor.c" in line for line in ctx.step("6.3").split("\n"))
    kept = PUBLISHED_NAMES - {"old_motor.c"}
    task.check(2, "6.1 archive is empty now: ls -la shows only . and ..",
               set(rows61) == {".", ".."} and all(r.kind == "d" for r in rows61.values()))
    task.check(2, "6.2 ls shows no archive folder", kept <= after["6.2"] and "archive" not in after["6.2"])
    task.check(1, "6.3 rm -i asked about old_motor.c", asked)
    task.check(2, "6.3 ls shows motor.c but no old_motor.c", kept <= after63 and "old_motor.c" not in after63)
    task.check(2, "6.4 ls shows src but no src_backup", kept <= after["6.4"] and "src_backup" not in after["6.4"])
    # an "it is gone" check holds for an untouched folder, so it only counts for a student whose pasted listing shows it too
    done62, done63, done64 = kept <= after["6.2"] and "archive" not in after["6.2"], kept <= after63 and "old_motor.c" not in after63, \
        kept <= after["6.4"] and "src_backup" not in after["6.4"]
    task.check(1, "archive is gone from your folder", lambda: done62 and ctx.facts.is_gone("archive"), needs_repo=True)
    task.check(1, "old_motor.c is gone from your folder", lambda: done63 and ctx.facts.is_gone("old_motor.c"), needs_repo=True)
    task.check(1, "src_backup is gone from your folder", lambda: done64 and ctx.facts.is_gone("src_backup"), needs_repo=True)
    shown64 = (kept - {"src"}) <= after["6.4"]  # the pasted listing shows the other lab files (src may be what went wrong)
    task.check(1, "src is untouched: every file the lab gave you is still there",
               lambda: shown64 and _intact(ctx, {"src"}), needs_repo=True)
    task.check(1, "the other lab files are untouched", lambda: shown64 and _intact(ctx, {"motor.c", "mission_log.txt", "README.txt", "tools"}),
               needs_repo=True)
    return task


def _hits_ok(ctx: Ctx, step: str, word: str) -> bool:
    return content.grep_hits(ctx.step(step)) in grep_sets(ctx, word)


def _count_ok(ctx: Ctx) -> bool:
    """ANSWER-5 is the number of lines the student's own 7.1 paste holds, and that paste is a correct search."""
    number, hits = lsparse.answer_number(ctx.text, 5), content.grep_hits(ctx.step("7.1"))
    return number is not None and number == len(hits) and hits in grep_sets(ctx, "TODO")


def grade_task7(ctx: Ctx) -> Task:
    """Search: grep -rn, find -name and find -delete."""
    task = Task(7, TITLES[7], MARKS[7], ctx.repo_mode)
    task.check(3, "7.1 grep -rn finds every line with the first search word, and only those", _hits_ok(ctx, "7.1", "TODO"))
    task.check(3, "7.2 grep -rn finds every line with the second search word, and only those",
               _hits_ok(ctx, "7.2", "import"))
    task.check(2, "7.3 find lists exactly the .py files", content.find_hits(ctx.step("7.3")) in find_sets(ctx, ".py"))
    task.check(2, "7.4 find lists the two compiled copies you made", content.find_hits(ctx.step("7.4")) == PYC_PAIR)
    task.check(2, "7.5 src/motor holds drivers and pwm.py again", names(ctx.step("7.5")) == children("src/motor"))
    task.check(1, "ANSWER-5 is the number of lines the first grep printed", _count_ok(ctx))
    task.check(1, "ANSWER-6 names the file with the most lines of the second search word",
               answer_only(ctx, 6, FACTS["most_imports_file"]))
    listed = names(ctx.step("7.5")) == children("src/motor")
    task.check(2, "no .pyc file is left in your folder",
               lambda: listed and (lambda walk: walk is not None and not [p for p in walk.paths if p.endswith(".pyc")])(ctx.facts.walk()),
               needs_repo=True)
    return task


def _py_lines_ok(ctx: Ctx, lines: Optional[list]) -> bool:
    return lines is not None and {"./" + line.lstrip("./") if not line.startswith("./") else line for line in lines} in find_sets(ctx, ".py")


def _log_size_ok(ctx: Ctx, size: int) -> bool:
    """The published size of the log, the size it has with Windows line ends, or its size in this clone."""
    published_size = len(published.FILES["mission_log.txt"].encode("ascii"))
    accepted = {published_size, published_size + len(LOG), ctx.facts.size("mission_log.txt")} - {None}
    return size in accepted


def grade_task8(ctx: Ctx) -> Task:
    """Productivity and report: Tab completion, a result saved with >, a signed summary."""
    task = Task(8, TITLES[8], MARKS[8], ctx.repo_mode)
    name = student_name(ctx)
    row = named_rows(ctx.step("8.1")).get("mission_log.txt")
    task.check(2, "8.1 the completed command printed the row of mission_log.txt with its size",
               row is not None and row.kind == "-" and _log_size_ok(ctx, row.size))
    task.check(3, "8.2 the list of .py files you saved is printed",
               content.find_hits(ctx.step("8.2")) in find_sets(ctx, ".py"))
    task.check(2, "8.3 cat shows your signed summary line", bool(name) and block(ctx, "8.3", [SUMMARY_PREFIX + name]))
    task.check(1, "py_files.txt in your folder lists the .py files",
               lambda: _py_lines_ok(ctx, ctx.facts.lines("py_files.txt")), needs_repo=True)
    task.check(2, "summary.txt in your folder holds your signed summary line",
               lambda: bool(name) and has_name(ctx, ctx.facts.lines("summary.txt"))
               and any(line.lower() == (SUMMARY_PREFIX + name).lower() for line in ctx.facts.lines("summary.txt") or []),
               needs_repo=True)
    return task
