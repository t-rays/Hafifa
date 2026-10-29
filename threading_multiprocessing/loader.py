"""Load required minutes from per-ticker timestamp text files."""

import pandas as pd
import os
from datetime import datetime
from logging import getLogger
from constants import TIMESTAMP_FLOOR, TIMESTAMP_FORMAT

logger = getLogger(__name__)


def format_timestamp(timestamp: str) -> datetime:
    """Parse one line as ``YYYY-MM-DD HH:MM:SS.ffffff``.

    Raises ``ValueError`` when the line does not match that format.
    """
    return datetime.strptime(timestamp, TIMESTAMP_FORMAT)

def strip_seconds_and_microseconds(timestamps: pd.Series) -> pd.Series:
    """Floor each timestamp to the start of its minute."""
    ts = pd.to_datetime(timestamps)
    return ts.dt.floor(TIMESTAMP_FLOOR)


def read_timestamps_from_txt(file_path: str) -> pd.Series:
    """Return minute-floored timestamps, one ``datetime`` per line.

    Raises ``FileNotFoundError`` when ``file_path`` does not exist,
    ``ValueError`` when a line cannot be parsed or the file has no lines.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File {file_path} not found")
    with open(file_path, "r", encoding="utf-8") as file:
        formatted_timestamps = pd.Series([format_timestamp(line.strip()) for line in file.readlines()])
    if formatted_timestamps.empty:
        raise ValueError(f"No timestamps in {file_path}")
    timestamps = strip_seconds_and_microseconds(formatted_timestamps)
    logger.debug(
        "Parsed %d timestamps from %s (%s to %s)",
        len(timestamps),
        file_path,
        timestamps.min(),
        timestamps.max(),
    )
    return timestamps
