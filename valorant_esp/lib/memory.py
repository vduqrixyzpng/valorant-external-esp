"""Thin wrapper around pymem for read-only external memory access.

Only reads are exposed — the aimbot/triggerbot modules call this to
resolve player coordinates from the game's actor array.
"""
from __future__ import annotations

from dataclasses import dataclass

try:
    import pymem
    import pymem.process
except ImportError:  # pragma: no cover - dev envs without pywin32
    pymem = None


@dataclass(slots=True)
class ModuleInfo:
    name: str
    base: int
    size: int


class ExternalMemory:
    def __init__(self, process_name: str) -> None:
        if pymem is None:
            raise RuntimeError("pymem not installed — pip install pymem pywin32")
        self.pm = pymem.Pymem(process_name)
        self._modules: dict[str, ModuleInfo] = {}

    def module(self, name: str) -> ModuleInfo:
        if name not in self._modules:
            mod = pymem.process.module_from_name(self.pm.process_handle, name)
            self._modules[name] = ModuleInfo(name, mod.lpBaseOfDll, mod.SizeOfImage)
        return self._modules[name]

    def read_ptr(self, addr: int) -> int:
        return int.from_bytes(self.pm.read_bytes(addr, 8), "little")

    def read_vec3(self, addr: int) -> tuple[float, float, float]:
        raw = self.pm.read_bytes(addr, 12)
        import struct
        return struct.unpack("<fff", raw)

    def read_i32(self, addr: int) -> int:
        return int.from_bytes(self.pm.read_bytes(addr, 4), "little", signed=True)

    def is_alive(self) -> bool:
        try:
            return self.pm.process_handle is not None
        except Exception:
            return False