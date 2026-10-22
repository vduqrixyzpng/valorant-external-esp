"""Rich-based logger setup for the interactive CLI."""
from __future__ import annotations

from rich.console import Console
from rich.logging import RichHandler
import logging

console = Console()


def setup_rich_logging(level: str = "INFO") -> None:
    logging.basicConfig(
        level=level,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(console=console, rich_tracebacks=True)],
    )