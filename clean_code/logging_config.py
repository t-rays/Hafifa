"""Logging configuration for the MP3 player."""

import logging

LOG_FORMAT = "%(levelname)s [%(name)s] %(message)s"


def configure_logging(level: int = logging.INFO) -> None:
    logging.basicConfig(level=level, format=LOG_FORMAT)
