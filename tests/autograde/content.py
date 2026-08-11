"""Readers for pasted file contents (cat, head, tail), grep -rn output and find output.

A pasted block is judged line by line: blank lines, shell prompts and the typed command are ignored, everything else
must be exactly the expected text. grep and find print their results in an order that differs between computers, so
those are read as sets. Everything is linear in the length of the pasted text and every line is cut to MAX_LINE
characters first, so a hostile pasted line cannot make the grader slow.
"""
from __future__ import annotations

import re
from typing import Dict, Iterable, List, Sequence, Set

MAX_LINE = 500
SIGILS = "$%>#"
GREP_RE = re.compile(r"^(\./[^:\s]+):(\d+):(.*)$")
FIND_RE = re.compile(r"^\./\S+$")


def pasted_lines(text: str) -> List[str]:
    """The non-blank lines of a pasted text, each cut to MAX_LINE characters and stripped at both ends."""
    return [line.strip() for line in (raw[:MAX_LINE] for raw in text.split("\n")) if line.strip()]


def looks_like_prompt(line: str) -> bool:
    """A shell prompt, with or without the command typed after it. A line that starts with # is a comment of a file,
    not a prompt, unless a prompt-looking word comes first (root@host:~# ...)."""
    tokens = line.split()
    if len(tokens) > 1 and "@" in tokens[0] and tokens[1].startswith(("MINGW", "MSYS", "UCRT", "CLANG")):
        return True  # the first line of Git Bash's two-line prompt
    for index, token in enumerate(tokens[:4]):
        if token in ("$", "%", ">"):
            return True
        if len(token) > 1 and token[-1] in SIGILS and any(c in token for c in "@:/~]"):
            return True
        if token == "#" and index > 0:
            return True
    return False


def block_matches(text: str, expected: Sequence[str], commands: Sequence[str] = ()) -> bool:
    """Is the pasted text exactly the expected lines, once blank lines, prompts and the typed commands are set aside?"""
    wanted = [line.strip() for line in expected]
    lines = pasted_lines(text)
    size = len(wanted)
    if not wanted or len(lines) < size:
        return False
    typed = {command.strip() for command in commands}
    others = [i for i, line in enumerate(lines) if not (looks_like_prompt(line) or line in typed)]
    first, last = (others[0], others[-1]) if others else (0, -1)
    for start in range(len(lines) - size + 1):
        if lines[start:start + size] == wanted and (not others or (first >= start and last < start + size)):
            return True
    return False


def without_questions(text: str) -> str:
    """The text without the lines that ask something (rm -i asks 'remove file?'): names are read from the rest."""
    return "\n".join(line for line in text.split("\n") if "?" not in line[:MAX_LINE])


def grep_hits(text: str) -> Set[str]:
    """The `./path:line:text` hits of a pasted `grep -rn` output."""
    hits: Set[str] = set()
    for raw in text.split("\n"):
        match = GREP_RE.match(raw[:MAX_LINE].strip())
        if match:
            hits.add(f"{match.group(1)}:{match.group(2)}:{match.group(3).rstrip()}")
    return hits


def find_hits(text: str) -> Set[str]:
    """The `./path` lines of a pasted `find` output."""
    found: Set[str] = set()
    for raw in text.split("\n"):
        line = raw[:MAX_LINE].strip()
        if FIND_RE.match(line) and not GREP_RE.match(line):
            found.add(line)
    return found


def grep_expected(files: Dict[str, str], word: str) -> Set[str]:
    """What `grep -rn word .` prints in robot-controller for these files (path below it -> text)."""
    hits: Set[str] = set()
    for path, text in files.items():
        lines = text.split("\n")
        if lines and lines[-1] == "":
            lines.pop()
        hits.update(f"./{path}:{number}:{line}" for number, line in enumerate(lines, start=1) if word in line)
    return hits


def find_expected(paths: Iterable[str], suffix: str) -> Set[str]:
    """What `find . -name "*<suffix>"` prints for these paths (below robot-controller)."""
    return {f"./{path}" for path in paths if path.endswith(suffix)}
