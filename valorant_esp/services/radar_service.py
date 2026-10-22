"""2D minimap radar state — translates world coords to a 200x200 dot array."""
from __future__ import annotations

from valorant_esp.services.entity_service import Entity


class RadarService:
    MAP_SIZE = 200.0
    SCALE = 0.02

    def __init__(self) -> None:
        self._dots: list[tuple[int, int, int]] = []

    def update(self, entities: list[Entity], local_team: int) -> None:
        self._dots = []
        for e in entities:
            if e.team == local_team:
                continue
            px = int(self.MAP_SIZE / 2 + e.origin.x * self.SCALE)
            py = int(self.MAP_SIZE / 2 - e.origin.y * self.SCALE)
            self._dots.append((px, py, e.health))

    @property
    def dots(self) -> list[tuple[int, int, int]]:
        return list(self._dots)