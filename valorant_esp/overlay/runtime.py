"""Main overlay loop: poll entities -> dispatch to features -> draw."""
from __future__ import annotations

import logging
import time

from valorant_esp.config.loader import CheatConfig
from valorant_esp.features import BoxESP, SkeletonESP, AimAssist
from valorant_esp.lib.input_hook import HotkeyListener
from valorant_esp.lib.offsets import OffsetTable
from valorant_esp.services.entity_service import EntityService
from valorant_esp.services.process_service import ProcessService
from valorant_esp.services.radar_service import RadarService

log = logging.getLogger(__name__)


class OverlayRuntime:
    def __init__(self, proc: ProcessService, cfg: CheatConfig) -> None:
        self.proc = proc
        self.cfg = cfg
        self.offsets = OffsetTable(cfg.offsets_path)
        self.entities = EntityService(proc.mem, self.offsets, cfg) if proc.mem else None
        self.radar = RadarService()
        self.box = BoxESP(cfg)
        self.skel = SkeletonESP(cfg)
        self.aim = AimAssist(cfg)
        self.hotkeys = HotkeyListener()
        self.hotkeys.bind(0x70, self._toggle_esp)   # F1
        self.hotkeys.bind(0x71, self._toggle_aim)   # F2
        self._running = False

    def _toggle_esp(self) -> None:
        self.cfg.features.esp_box = not self.cfg.features.esp_box
        log.info("esp_box=%s", self.cfg.features.esp_box)

    def _toggle_aim(self) -> None:
        self.cfg.features.aimbot = not self.cfg.features.aimbot
        log.info("aimbot=%s", self.cfg.features.aimbot)

    def run(self) -> None:
        self._running = True
        tick = 1.0 / max(1, self.cfg.refresh_hz)
        while self._running:
            t0 = time.perf_counter()
            self.hotkeys.poll()
            if self.entities and self.proc.ready:
                snap = self.entities.snapshot()
                self.radar.update(snap, self.entities.local_team)
            time.sleep(max(0.0, tick - (time.perf_counter() - t0)))

    def stop(self) -> None:
        self._running = False