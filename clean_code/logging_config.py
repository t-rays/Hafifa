"""Logging configuration for the MP3 player."""

import logging

LOG_FORMAT = "%(levelname)s [%(name)s] %(message)s"


def configure_logging(level: int = logging.INFO) -> None:
    """Configure root logging once before the application UI starts.

    Args:
        level: Minimum severity written to stderr (default ``INFO``).
    """
    logging.basicConfig(level=level, format=LOG_FORMAT)
