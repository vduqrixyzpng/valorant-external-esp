"""Aim assist stub — demonstrates FOV-based target selection.

Kept intentionally non-functional: the actual mouse movement hook is
commented out so this module can ship without triggering anti-cheat
heuristics. Study the target-picker logic; wire your own input for
offline practice.
"""
from __future__ import annotations

import math
import logging

from valorant_esp.config.loader import CheatConfig
from valorant_esp.services.entity_service import Entity
from valorant_esp.lib.vector import Vec3

log = logging.getLogger(__name__)


class AimAssist:
    def __init__(self, cfg: CheatConfig, fov_degrees: float = 3.0) -> None:
        self.cfg = cfg
        self.fov = fov_degrees

    def _angle_between(self, a: Vec3, b: Vec3) -> float:
        dot = a.dot(b)
        la, lb = a.length, b.length
        if la == 0 or lb == 0:
            return 180.0
        return math.degrees(math.acos(max(-1.0, min(1.0, dot / (la * lb)))))

    def pick_target(self, entities: list[Entity], view_dir: Vec3, local_team: int) -> Entity | None:
        if not self.cfg.features.aimbot:
            return None
        best: tuple[float, Entity] | None = None
        for e in entities:
            if e.team == local_team:
                continue
            angle = self._angle_between(view_dir, Vec3(e.head.x, e.head.y, e.head.z))
            if angle > self.fov:
                continue
            if best is None or angle < best[0]:
                best = (angle, e)
        # NOTE: mouse_move(best[1].head) intentionally not implemented.
        return best[1] if best else None