"""2D bounding-box ESP — projects each enemy's head/foot to screen space."""
from __future__ import annotations

from valorant_esp.config.loader import CheatConfig
from valorant_esp.lib.vector import Vec3, world_to_screen
from valorant_esp.services.entity_service import Entity


class BoxESP:
    def __init__(self, cfg: CheatConfig) -> None:
        self.cfg = cfg
        self.color_visible = (0, 255, 0, 255)
        self.color_hidden = (255, 0, 0, 255)

    def draw(self, entities: list[Entity], view_matrix: list[float], w: int, h: int, local_team: int) -> list[tuple]:
        boxes: list[tuple] = []
        if not self.cfg.features.esp_box:
            return boxes
        for e in entities:
            if e.team == local_team:
                continue
            head = world_to_screen(e.head, view_matrix, w, h)
            foot = world_to_screen(Vec3(e.origin.x, e.origin.y, e.origin.z - 65.0), view_matrix, w, h)
            if not head or not foot:
                continue
            height = foot[1] - head[1]
            width = int(height * 0.55)
            boxes.append((head[0] - width // 2, head[1], width, height, self.color_hidden))
        return boxes