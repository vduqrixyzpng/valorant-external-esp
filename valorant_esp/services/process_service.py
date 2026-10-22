"""Handles attaching to the VALORANT client and validating the module base."""
from __future__ import annotations

import logging

from valorant_esp.config.loader import CheatConfig
from valorant_esp.lib.memory import ExternalMemory, ModuleInfo

log = logging.getLogger(__name__)


class ProcessService:
    def __init__(self, cfg: CheatConfig) -> None:
        self.cfg = cfg
        self.mem: ExternalMemory | None = None
        self.client_base: ModuleInfo | None = None

    def attach(self, exe_name: str) -> bool:
        try:
            self.mem = ExternalMemory(exe_name)
        except Exception as exc:
            log.warning("attach failed: %s", exc)
            return False
        self.client_base = self.mem.module(exe_name.replace("-Win64-Shipping", ""))
        log.info("attached to %s @ 0x%X", exe_name, self.client_base.base)
        return True

    @property
    def ready(self) -> bool:
        return self.mem is not None and self.mem.is_alive()