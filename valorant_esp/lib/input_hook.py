"""Global hotkey hooks for toggling ESP / aimbot at runtime (F1..F8)."""
from __future__ import annotations

import ctypes
from ctypes import wintypes
from typing import Callable


class HotkeyListener:
    def __init__(self) -> None:
        self._bindings: dict[int, Callable[[], None]] = {}
        self._user32 = ctypes.windll.user32

    def bind(self, vk_code: int, cb: Callable[[], None]) -> None:
        self._bindings[vk_code] = cb

    def poll(self) -> None:
        for vk, cb in self._bindings.items():
            if self._user32.GetAsyncKeyState(vk) & 0x8000:
                try:
                    cb()
                except Exception:
                    pass