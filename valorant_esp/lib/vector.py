"""Small 3D vector math helpers used by the ESP projection code."""
from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Vec3:
    x: float
    y: float
    z: float

    def __add__(self, o: "Vec3") -> "Vec3":
        return Vec3(self.x + o.x, self.y + o.y, self.z + o.z)

    def __sub__(self, o: "Vec3") -> "Vec3":
        return Vec3(self.x - o.x, self.y - o.y, self.z - o.z)

    def dot(self, o: "Vec3") -> float:
        return self.x * o.x + self.y * o.y + self.z * o.z

    @property
    def length(self) -> float:
        return math.sqrt(self.dot(self))


def world_to_screen(world: Vec3, view_matrix: list[float], width: int, height: int) -> tuple[int, int] | None:
    """Project a world-space point to screen pixels using the game's 4x4 view matrix."""
    w = view_matrix[12] * world.x + view_matrix[13] * world.y + view_matrix[14] * world.z + view_matrix[15]
    if w < 0.001:
        return None
    x = view_matrix[0] * world.x + view_matrix[1] * world.y + view_matrix[2] * world.z + view_matrix[3]
    y = view_matrix[4] * world.x + view_matrix[5] * world.y + view_matrix[6] * world.z + view_matrix[7]
    return (int((width / 2) * (x / w + 1)), int((height / 2) * (1 - y / w)))