"""ImGui-style overlay renderer stub.

Real implementation would use pyimgui + glfw; this module keeps the
interface so feature modules can be unit tested without a GPU context.
"""
from __future__ import annotations


class DummyRenderer:
    def __init__(self, width: int = 1920, height: int = 1080) -> None:
        self.width = width
        self.height = height
        self._commands: list[tuple] = []

    def rect(self, x: int, y: int, w: int, h: int, color: tuple[int, int, int, int]) -> None:
        self._commands.append(("rect", x, y, w, h, color))

    def line(self, x1: int, y1: int, x2: int, y2: int, color: tuple[int, int, int, int]) -> None:
        self._commands.append(("line", x1, y1, x2, y2, color))

    def text(self, x: int, y: int, text: str) -> None:
        self._commands.append(("text", x, y, text))

    def flush(self) -> None:
        self._commands.clear()