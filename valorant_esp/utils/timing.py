"""Frame-timing helpers used by the overlay runtime."""
from __future__ import annotations

import time
from contextlib import contextmanager
from typing import Iterator


@contextmanager
def frame_budget(hz: int) -> Iterator[None]:
    t0 = time.perf_counter()
    yield
    budget = 1.0 / max(1, hz)
    elapsed = time.perf_counter() - t0
    if elapsed < budget:
        time.sleep(budget - elapsed)


def now_ms() -> int:
    return int(time.perf_counter() * 1000)