"""Weapon metadata table (name -> damage / fire-rate) for ESP tooltips."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class WeaponInfo:
    name: str
    damage_head: int
    damage_body: int
    fire_rate: float


WEAPONS: dict[str, WeaponInfo] = {
    "Vandal": WeaponInfo("Vandal", 160, 40, 9.75),
    "Phantom": WeaponInfo("Phantom", 156, 39, 11.0),
    "Operator": WeaponInfo("Operator", 255, 150, 0.6),
    "Sheriff": WeaponInfo("Sheriff", 159, 55, 4.0),
}
</parameter>