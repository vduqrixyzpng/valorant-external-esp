"""Serializable player snapshot mirroring the in-game actor state we read."""
from __future__ import annotations

from dataclasses import dataclass, asdict


@dataclass(slots=True)
class PlayerSnapshot:
    index: int
    team: int
    agent: str
    health: int
    armor: int
    position: tuple[float, float, float]
    is_visible: bool = False

    def to_dict(self) -> dict:
        return asdict(self)