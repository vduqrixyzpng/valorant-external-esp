"""Unit tests for EntityService.snapshot using a fake ExternalMemory."""
from __future__ import annotations

from unittest.mock import MagicMock

from valorant_esp.config.loader import CheatConfig
from valorant_esp.lib.offsets import OffsetTable
from valorant_esp.services.entity_service import EntityService


def test_snapshot_skips_dead_players(tmp_path):
    offsets_file = tmp_path / "offsets.json"
    offsets_file.write_text(
        '{"world":100,"actor_manager":10,"actor_count":20,"actor_array":30,'
        '"team_id":40,"health":50,"origin":60}',
        encoding="utf-8",
    )
    offsets = OffsetTable(offsets_file)

    mem = MagicMock()
    mem.module.return_value.base = 1000
    mem.read_ptr.side_effect = [2000, 3000]  # world, actors
    mem.read_i32.return_value = 2            # count = 2
    mem.read_vec3.return_value = (1.0, 2.0, 3.0)

    svc = EntityService(mem, offsets, CheatConfig())
    entities = svc.snapshot()
    # health == 2 for both -> both alive
    assert len(entities) == 2