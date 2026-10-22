"""Dev helper — dumps the current module base + view matrix for debugging.

Do not run against live Valorant; use the offline training range or your
own test binary. Output is written to dumps/<timestamp>.json.
"""
from __future__ import annotations

import json
import time
from pathlib import Path

from valorant_esp.lib.memory import ExternalMemory
from valorant_esp.lib.offsets import OffsetTable


def main() -> None:
    mem = ExternalMemory("VALORANT-Win64-Shipping.exe")
    offsets = OffsetTable(Path("config/offsets.json"))
    client = mem.module("VALORANT")
    out = {
        "dumped_at": time.time(),
        "client_base": hex(client.base),
        "world": hex(mem.read_ptr(client.base + offsets["world"])),
    }
    Path("dumps").mkdir(exist_ok=True)
    Path(f"dumps/{int(time.time())}.json").write_text(json.dumps(out, indent=2))
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
</parameter>