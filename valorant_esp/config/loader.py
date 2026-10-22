"""Config loader — merges default.toml with local overrides and CLI flags."""
from __future__ import annotations

import tomllib
from dataclasses import dataclass, field
from pathlib import Path


@dataclass(slots=True)
class FeatureFlags:
    esp_box: bool = True
    esp_skeleton: bool = True
    esp_health: bool = True
    aimbot: bool = False          # disabled by default — educational sprint only
    radar_hud: bool = False
    stream_proof: bool = True     # hides overlay from OBS capture


@dataclass(slots=True)
class CheatConfig:
    log_level: str = "INFO"
    acknowledge_educational_only: bool = False
    refresh_hz: int = 60
    overlay_alpha: float = 0.85
    features: FeatureFlags = field(default_factory=FeatureFlags)
    offsets_path: Path = Path("config/offsets.json")


def load_config(path: Path, overrides: list[str] | None = None) -> CheatConfig:
    cfg = CheatConfig()
    if path.exists():
        raw = tomllib.loads(path.read_text(encoding="utf-8"))
        for k, v in raw.get("core", {}).items():
            if hasattr(cfg, k):
                setattr(cfg, k, v)
        for k, v in raw.get("features", {}).items():
            if hasattr(cfg.features, k):
                setattr(cfg.features, k, bool(v))
    if overrides:
        for flag in overrides:
            if flag.startswith("--off") and flag[5:] in {f.name for f in FeatureFlags.__dataclass_fields__.values()}:
                setattr(cfg.features, flag[5:], False)
    return cfg