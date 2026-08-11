"""Helpers for reading the text a student pasted into submission/outputs.txt."""
from __future__ import annotations

import re
from typing import Dict, List, Optional, Sequence

ANSI_RE = re.compile(r"\x1b\[[0-9;?]*[A-Za-z]")
BOUNDARY_RE = re.compile(r"^(?:---\s*(\d+\.\d+)\b.*|===\s*TASK\b.*)$", re.MULTILINE)
PLACEHOLDER = "(paste output here)"
QUESTION_RE = re.compile(r"^(?:# Q\d+ |ANSWER-\d+\s*:)")  # the question and answer lines that sit between steps
HEADER_RE = re.compile(r"^---\s*(\d+\.\d+)\s+(.*?)\s*---\s*$")
THEN = "   then   "
MAX_LINE = 500
PROMPT_SIGNS = "$%>#\u276f\u279c\u00bb"  # the signs a prompt ends in, starship and oh-my-zsh arrows included


def normalise(text: str) -> str:
    """Remove colour codes and carriage returns and strip trailing blanks."""
    text = ANSI_RE.sub("", text)
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    return "\n".join(line.rstrip() for line in text.split("\n"))


def parse_steps(text: str) -> Dict[str, str]:
    """Split the submission into {step id: pasted text}, e.g. {"2.3": "..."}."""
    steps: Dict[str, str] = {}
    matches = list(BOUNDARY_RE.finditer(text))
    for index, match in enumerate(matches):
        step_id = match.group(1)
        if step_id is None:
            continue
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        body = text[match.end():end]
        kept = [line for line in body.split("\n") if line.strip() != PLACEHOLDER and not QUESTION_RE.match(line)]
        body = "\n".join(kept).strip("\n")
        steps[step_id] = (steps[step_id] + "\n" + body) if step_id in steps else body
    return steps


def header_field(text: str, label: str) -> str:
    """Return the value of a 'Label : value' line near the top of the file."""
    match = re.search(rf"^{label}\s*:[ \t]*(.*)$", text, re.MULTILINE | re.IGNORECASE)
    return match.group(1).strip() if match else ""


def get_answer(text: str, number: int) -> str:
    """Return the student's ANSWER-<number> value ('' if blank or a placeholder)."""
    match = re.search(rf"^ANSWER-{number}[ \t]*:[ \t]*(.*)$", text, re.MULTILINE)
    if not match:
        return ""
    value = match.group(1).strip().strip("`'\" ")
    return "" if value.startswith("<") else value


def safe_text(text: str) -> str:
    """Remove control characters (ESC, BEL, newlines, ...) so student-written text cannot steer a terminal."""
    return re.sub(r"[\x00-\x1f\x7f-\x9f]", "", text)


def all_step_commands(text: str) -> Dict[str, List[str]]:
    """The commands the template names in the header line of every step ('--- 6.3  rm -i old_motor.c   then   ls ---')."""
    found: Dict[str, List[str]] = {}
    for line in text.split("\n"):
        match = HEADER_RE.match(line[:MAX_LINE])
        if match and match.group(1) not in found:
            found[match.group(1)] = [part.strip() for part in match.group(2).split(THEN) if part.strip()]
    return found


def step_commands(text: str, step_id: str) -> List[str]:
    """The commands of one step ([] if the step is not in the text)."""
    return all_step_commands(text).get(step_id, [])


def echo_prefix(line: str, commands: Sequence[str]) -> Optional[str]:
    """If 'line' is a prompt followed by one of the typed commands, the prompt before the command ('' for a bare command);
    None if it is not an echo of a typed command. The command must start after a space or a prompt sign."""
    stripped = line[:MAX_LINE].strip()
    for command in sorted(commands, key=len, reverse=True):
        if stripped == command:
            return ""
        if stripped.endswith(command) and len(stripped) > len(command):
            before = stripped[:-len(command)]
            if before[-1].isspace() or before[-1] in PROMPT_SIGNS:
                return before.rstrip()
    return None


def strip_prompts(steps: Dict[str, str], text: str) -> Dict[str, str]:
    """The pasted steps without the lines a terminal copy adds around the output: the prompt with the typed command, and
    the prompt that waits after it (the same prompt text shows before every command, whatever shell the student uses)."""
    commands = all_step_commands(text)
    prefixes = set()
    for step_id, body in steps.items():
        for line in body.split("\n"):
            prefix = echo_prefix(line, commands.get(step_id, []))
            if prefix:
                prefixes.add(prefix)
    cleaned: Dict[str, str] = {}
    for step_id, body in steps.items():
        kept = [line for line in body.split("\n")
                if echo_prefix(line, commands.get(step_id, [])) is None and line[:MAX_LINE].strip() not in prefixes]
        cleaned[step_id] = "\n".join(kept).strip("\n")
    return cleaned
