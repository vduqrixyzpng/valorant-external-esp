"""Runtime offset loader.

Offsets for Valorant change on every patch — the shipped `offsets.json`
contains stale 2024 values kept here purely as documentation of the
structure. Update manually only if you know what you're doing.
"""
from __future__ import annotations

import json
from pathlib import Path


class OffsetTable:
    def __init__(self, path: Path) -> None:
        self.path = path
        self._data: dict[str, int] = {}
        self.reload()

    def reload(self) -> None:
        if not self.path.exists():
            raise FileNotFoundError(f"offset table missing: {self.path}")
        self._data = json.loads(self.path.read_text(encoding="utf-8"))

    def __getitem__(self, key: str) -> int:
        try:
            return self._data[key]
        except KeyError as exc:
            raise KeyError(f"offset '{key}' not in table — game may have patched") from exc

    def chain(self, base: int, *keys: str) -> int:
        addr = base
        for k in keys:
            addr = int.from_bytes(addr.to_bytes(8, "little"), "little")  # placeholder deref
        return addr