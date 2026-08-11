"""Read-only facts about the student's robot-controller folder. Nothing here runs student code or follows a link."""
from __future__ import annotations

import os
import stat
from typing import Dict, List, NamedTuple, Optional, Set

from .taskinfo import RC
from .textutil import safe_text

MAX_ENTRIES = 600
MAX_DEPTH = 8
MAX_READ = 65536
IGNORED = {".DS_Store"}  # Finder adds one on a Mac; it is nobody's mistake


class Walk(NamedTuple):
    """What a recursive search of robot-controller sees."""

    files: Dict[str, str]  # regular text files (path below robot-controller -> text), as grep -r reads them
    paths: Set[str]        # every file, link or other entry that is not a folder, as find lists them


class Facts:
    """Live facts about one clone (repo=None means there is no clone: only published values are known)."""

    def __init__(self, repo: Optional[str]) -> None:
        self.repo = os.path.abspath(repo) if repo and os.path.isdir(repo) else None
        self._walk: Optional[Walk] = None
        self._walked = False

    @property
    def rc(self) -> Optional[str]:
        """The robot-controller folder of the clone."""
        return os.path.join(self.repo, RC) if self.repo else None

    def path(self, rel: str) -> Optional[str]:
        """Absolute path of 'rel' below robot-controller; None when there is no clone, nothing is there, or a
        symbolic link lies on the way (a link is never followed)."""
        if not self.repo:
            return None
        current = self.repo
        for part in [RC] + [p for p in rel.split("/") if p]:
            current = os.path.join(current, part)
            try:
                if stat.S_ISLNK(os.lstat(current).st_mode):
                    return None
            except OSError:
                return None
        return current

    def is_gone(self, rel: str) -> bool:
        """Is nothing (no file, folder or link) at 'rel' below robot-controller? Only answers yes for a real
        robot-controller folder that can be looked into: without a clone, or behind a link, nothing counts as gone."""
        root = self.path("")
        if root is None or not stat.S_ISDIR(os.lstat(root).st_mode):
            return False
        return not os.path.lexists(os.path.join(root, *[p for p in rel.split("/") if p]))

    def size(self, rel: str) -> Optional[int]:
        """Size of a regular file (a link, folder or missing file gives None)."""
        target = self.path(rel)
        if target is None:
            return None
        info = os.lstat(target)
        return info.st_size if stat.S_ISREG(info.st_mode) else None

    def read(self, rel: str) -> Optional[str]:
        """The text of a small regular file, control characters kept; None for a link, device, folder or missing file."""
        target = self.path(rel)
        if target is None:
            return None
        return self._read_file(target)

    @staticmethod
    def _read_file(target: str) -> Optional[str]:
        flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_NONBLOCK", 0)
        try:
            descriptor = os.open(target, flags)
        except OSError:
            return None
        with os.fdopen(descriptor, "rb") as handle:
            if not stat.S_ISREG(os.fstat(handle.fileno()).st_mode):
                return None
            data = handle.read(MAX_READ)
        return data.decode("utf-8", errors="replace").replace("\r\n", "\n")

    def lines(self, rel: str) -> Optional[List[str]]:
        """The non-blank lines of a small text file, stripped, control characters removed (None if unreadable)."""
        text = self.read(rel)
        if text is None:
            return None
        return [line.strip() for line in (safe_text(raw) for raw in text.split("\n")) if line.strip()]

    def names(self, rel_dir: str) -> Optional[Set[str]]:
        """The entry names of a real folder below robot-controller (without a Finder .DS_Store); None if it is
        missing, a link, or unreadable."""
        target = self.path(rel_dir)
        if target is None:
            return None
        try:
            with os.scandir(target) as entries:
                found = {entry.name for entry in entries}
        except OSError:
            return None
        return found - IGNORED

    def walk(self) -> Optional[Walk]:
        """Search robot-controller the way grep -r and find do: links are listed but never followed. None when there is
        no clone or robot-controller is missing or a link."""
        if self._walked:
            return self._walk
        self._walked = True
        root = self.path("")
        if root is None or not stat.S_ISDIR(os.lstat(root).st_mode):
            return None
        files: Dict[str, str] = {}
        paths: Set[str] = set()
        queue: List[tuple] = [(root, "", 0)]
        seen = 0
        while queue and seen < MAX_ENTRIES:
            folder, prefix, depth = queue.pop(0)
            try:
                with os.scandir(folder) as entries:
                    ordered = sorted(entries, key=lambda e: e.name)
            except OSError:
                continue
            for entry in ordered:
                if seen >= MAX_ENTRIES:
                    break
                seen += 1
                rel = prefix + entry.name
                if entry.name in IGNORED:
                    continue
                if entry.is_symlink():
                    paths.add(rel)
                elif entry.is_dir(follow_symlinks=False):
                    if depth < MAX_DEPTH:
                        queue.append((entry.path, rel + "/", depth + 1))
                else:
                    paths.add(rel)
                    text = self._read_file(entry.path)
                    if text is not None and "\x00" not in text:
                        files[rel] = text
        self._walk = Walk(files, paths)
        return self._walk

    def is_this_clone(self, path: str) -> bool:
        """Is the pasted folder path this clone's robot-controller (the same folder on this computer)?"""
        if not self.rc:
            return False
        try:
            return os.path.samefile(path, self.rc)
        except (OSError, ValueError):  # ValueError: a pasted path with an embedded NUL byte
            return False
