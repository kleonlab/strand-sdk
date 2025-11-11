"""Centralized logging helpers."""

from __future__ import annotations

import logging
from typing import Final

_LOGGER_NAME: Final = "strand"

# Configure root logger once at module import time
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def get_logger(component: str | None = None) -> logging.Logger:
    """Get a logger for the given component.

    Args:
        component: Component name (e.g., "optimizer", "cli"). If None, returns root strand logger.

    Returns:
        Configured logger instance.
    """
    name = f"{_LOGGER_NAME}.{component}" if component else _LOGGER_NAME
    return logging.getLogger(name)
