"""Tickers, OHLCV frames, and in-memory stock state."""

from dataclasses import dataclass, field
from enum import StrEnum

import pandas as pd

from core.constant import OHLCV_COLUMNS


class StockTicker(StrEnum):
    """Yahoo Finance symbols for the exercise stocks."""

    BITCOIN = "BTC-USD"
    GOOGLE = "GOOGL"
    AMAZON = "AMZN"

    @property
    def display_name(self) -> str:
        """Title-cased report label, for example ``Bitcoin``."""
        return self.name.title()


def empty_ohlcv_frame() -> pd.DataFrame:
    """Empty OHLCV frame with a ``time`` index."""
    return pd.DataFrame(
        columns=list(OHLCV_COLUMNS),
        index=pd.DatetimeIndex([], name="time"),
    )


def as_ohlcv_frame(frame: pd.DataFrame) -> pd.DataFrame:
    """Normalize a Yahoo frame to ``OHLCV_COLUMNS`` and a naive UTC ``time`` index.

    Flattens MultiIndex columns and sorts by time.

    Raises:
        KeyError: If a required OHLCV column is missing.
    """
    if isinstance(frame.columns, pd.MultiIndex):
        frame = frame.copy()
        frame.columns = frame.columns.get_level_values(0)
    frame = frame.loc[:, list(OHLCV_COLUMNS)]
    index = pd.DatetimeIndex(frame.index)
    if index.tz is not None:
        index = index.tz_convert("UTC").tz_localize(None)
    frame.index = index
    frame.index.name = "time"
    return frame.sort_index()


@dataclass
class Stock:
    """One ticker, its requested hours, and any fetched OHLCV bars.

    Attributes:
        hours: Timestamps loaded from a dates file.
        data: Fetched hourly bars; empty until the pipeline runs.
    """

    ticker: StockTicker
    hours: pd.DatetimeIndex
    data: pd.DataFrame = field(default_factory=empty_ohlcv_frame)

    @property
    def name(self) -> str:
        """Report label for this stock (``ticker.display_name``)."""
        return self.ticker.display_name
