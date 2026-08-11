"""Small checks on pasted listings and file contents that several task graders share."""
from __future__ import annotations

from typing import Dict, Iterable, List, Optional, Set

from . import content, lsparse, published
from .context import Ctx
from .lsparse import LsRow
from .taskinfo import NOTES_FINAL
from .textutil import header_field, safe_text, step_commands

PUBLISHED_NAMES: Set[str] = {path.split("/")[0] for path in published.FILES}
OTHER_FILE_NAMES: Set[str] = {path.rsplit("/", 1)[-1] for path in published.FILES}


def student_name(ctx: Ctx) -> str:
    """The Name line of outputs.txt, safe to print."""
    return safe_text(header_field(ctx.text, "Name"))


def block(ctx: Ctx, step: str, expected: List[str]) -> bool:
    """Is the text pasted for 'step' exactly the expected lines (prompts and the typed command aside)?"""
    return content.block_matches(ctx.step(step), expected, step_commands(ctx.text, step))


def named_rows(text: str) -> Dict[str, LsRow]:
    """The long-format rows of a pasted listing, by name."""
    return {row.name: row for row in lsparse.parse_ls_rows(text)}


def names(text: str) -> Set[str]:
    """The names a pasted short listing shows (a question like rm -i's is set aside, and so is a Finder .DS_Store)."""
    return {n for n in lsparse.plain_names(content.without_questions(text)) if n != ".DS_Store"}


def top_level(kind: str) -> Set[str]:
    """The published top-level entries of robot-controller of one kind: '-' files or 'd' folders."""
    folders = {path.split("/")[0] for path in published.FILES if "/" in path}
    return folders if kind == "d" else PUBLISHED_NAMES - folders


def rows_show(text: str, files: Iterable[str], folders: Iterable[str]) -> bool:
    """Every name is listed as a `-` row (files) or a `d` row (folders)."""
    rows = named_rows(text)
    return (all(n in rows and rows[n].kind == "-" for n in files)
            and all(n in rows and rows[n].kind == "d" for n in folders))


def children(rel_dir: str) -> Set[str]:
    """The published names inside a folder of robot-controller."""
    prefix = rel_dir.rstrip("/") + "/"
    return {path[len(prefix):].split("/")[0] for path in published.FILES if path.startswith(prefix)}


def perfect_files() -> Dict[str, str]:
    """The files of robot-controller as a perfect student leaves them for the searches (notes.txt rewritten)."""
    files = dict(published.FILES)
    files["notes.txt"] = "\n".join(NOTES_FINAL) + "\n"
    return files


def _src_copy(files: Dict[str, str]) -> Dict[str, str]:
    """What `cp -r src src_backup` adds."""
    return {"src_backup/" + path[len("src/"):]: text for path, text in files.items() if path.startswith("src/")}


def search_states() -> List[Dict[str, str]]:
    """The folders a student may be searching, whatever order the tasks were done in (a task done late leaves its
    mark on the folder): notes.txt as given or rewritten by Task 2, with or without the copy src_backup of Task 4."""
    states = []
    for notes in (published.FILES["notes.txt"], "\n".join(NOTES_FINAL) + "\n"):
        for copy in (False, True):
            files = dict(published.FILES)
            files["notes.txt"] = notes
            if copy:
                files.update(_src_copy(files))
            states.append(files)
    return states


# the extra .py file a student has between Tasks 4 and 6: sensor_backup.py, then sensor_old.py, then archive/sensor_old.py
_PY_COPIES = ([], ["sensor_backup.py"], ["sensor_old.py"], ["archive/sensor_old.py"])


def grep_sets(ctx: Ctx, word: str) -> List[Set[str]]:
    """The hit sets a correct `grep -rn word .` may print: any state of search_states(), and what the live folder holds."""
    sets = [content.grep_expected(files, word) for files in search_states()]
    walked = ctx.facts.walk() if ctx.repo_mode else None
    if walked is not None:
        sets.append(content.grep_expected(walked.files, word))
    return sets


def find_sets(ctx: Ctx, suffix: str) -> List[Set[str]]:
    """The path sets a correct `find . -name "*<suffix>"` may print."""
    sets = []
    for files in search_states():
        for extra in _PY_COPIES:
            sets.append(content.find_expected(list(files) + extra, suffix))
    walked = ctx.facts.walk() if ctx.repo_mode else None
    if walked is not None:
        sets.append(content.find_expected(walked.paths, suffix))
    return sets


def answer_only(ctx: Ctx, number: int, wanted: str) -> bool:
    """The answer names the wanted file and no other file of the folder (a hedged list of names does not count)."""
    others = OTHER_FILE_NAMES - {wanted}
    return lsparse.answer_is(ctx.text, number, wanted) and not any(lsparse.answer_is(ctx.text, number, o) for o in others)


def has_name(ctx: Ctx, lines: Optional[List[str]]) -> bool:
    """Does one of the (non-link) file's lines contain the student's name?"""
    name = student_name(ctx).lower()
    return bool(name) and lines is not None and any(name in line.lower() for line in lines)
