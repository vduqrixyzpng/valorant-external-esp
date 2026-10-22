"""Skeleton ESP — draws bone-to-bone lines using the actor's bone matrix."""
from __future__ import annotations

from valorant_esp.config.loader import CheatConfig
from valorant_esp.lib.vector import world_to_screen

BONE_CHAINS: list[tuple[int, int]] = [
    (0, 1), (1, 2), (2, 3),        # spine
    (3, 4), (4, 5), (5, 6),        # neck -> head
    (3, 7), (7, 8), (8, 9),        # right arm
    (3, 10), (10, 11), (11, 12),   # left arm
    (0, 13), (13, 14), (14, 15),   # right leg
    (0, 16), (16, 17), (17, 18),   # left leg
]


class SkeletonESP:
    def __init__(self, cfg: CheatConfig) -> None:
        self.cfg = cfg

    def project_bones(self, bones_world: list[tuple[float, float, float]], view_matrix: list[float], w: int, h: int) -> list[tuple[int, int, int, int]]:
        if not self.cfg.features.esp_skeleton:
            return []
        pts = [world_to_screen(type("V", (), {"x": b[0], "y": b[1], "z": b[2]})(), view_matrix, w, h) for b in bones_world]
        segments: list[tuple[int, int, int, int]] = []
        for a, b in BONE_CHAINS:
            if a < len(pts) and b < len(pts) and pts[a] and pts[b]:
                segments.append((pts[a][0], pts[a][1], pts[b][0], pts[b][1]))
        return segments