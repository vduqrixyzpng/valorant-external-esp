"""Entry point wiring for the external cheat toolkit.

Loads config, spins up the process attach service, and hands control to
the overlay runtime. Run with `python -m valorant_esp.bootstrap`.
"""
from __future__ import annotations

import logging
import sys
from pathlib import Path

from valorant_esp.config.loader import load_config
from valorant_esp.services.process_service import ProcessService
from valorant_esp.overlay.runtime import OverlayRuntime

log = logging.getLogger("valorant_esp")


def main(argv: list[str] | None = None) -> int:
    argv = argv or sys.argv[1:]
    cfg = load_config(Path("config/default.toml"), overrides=argv)

    logging.basicConfig(
        level=cfg.log_level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )
    log.info("valorant-external-esp v%s starting", __import__("valorant_esp").__version__)

    if not cfg.acknowledge_educational_only:
        log.error("Refusing to run: set acknowledge_educational_only = true in config.")
        return 2

    proc = ProcessService(cfg)
    if not proc.attach("VALORANT-Win64-Shipping.exe"):
        log.warning("Valorant process not found — running overlay in offline demo mode.")

    runtime = OverlayRuntime(proc, cfg)
    try:
        runtime.run()
    except KeyboardInterrupt:
        log.info("Shutdown requested")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())