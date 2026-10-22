"""Walks the actor array and produces a snapshot of visible players.

Feeds the ESP overlay (box + skeleton) and the aimbot target picker.
Read-only — no memory writes.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass

from valorant_esp.config.loader import CheatConfig
from valorant_esp.lib.memory import ExternalMemory
from valorant_esp.lib.offsets import OffsetTable
from valorant_esp.lib.vector import Vec3

log = logging.getLogger(__name__)


@dataclass(slots=True)
class Entity:
    index: int
    team: int
    health: int
    origin: Vec3
    head: Vec3
    distance: float


class EntityService:
    def __init__(self, mem: ExternalMemory, offsets: OffsetTable, cfg: CheatConfig) -> None:
        self.mem = mem
        self.offsets = offsets
        self.cfg = cfg
        self.local_team: int = 0

    def snapshot(self) -> list[Entity]:
        out: list[Entity] = []
        try:
            world = self.mem.read_ptr(self.mem.module("VALORANT").base + self.offsets["world"])
            actors = self.mem.read_ptr(world + self.offsets["actor_manager"])
            count = self.mem.read_i32(actors + self.offsets["actor_count"])
        except Exception as exc:
            log.debug("entity walk aborted: %s", exc)
            return out

        for i in range(min(count, 64)):
            try:
                actor = self.mem.read_ptr(actors + self.offsets["actor_array"] + i * 8)
                if not actor:
                    continue
                team = self.mem.read_i32(actor + self.offsets["team_id"])
                hp = self.mem.read_i32(actor + self.offsets["health"])
                if hp <= 0:
                    continue
                origin = Vec3(*self.mem.read_vec3(actor + self.offsets["origin"]))
                head = Vec3(origin.x, origin.y, origin.z + 65.0)
                out.append(Entity(i, team, hp, origin, head, origin.length))
            except Exception:
                continue
        return out