"""Runtime settings: tickers, timestamp files, output path, and worker count."""

from models import StockTicker
from typing import List, Dict
import os
from logging import getLogger
from dotenv import load_dotenv
from constants import (
    DEFAULT_DESTINATION_FILE_PATH,
    DEFAULT_MAX_WORKERS,
    DEFAULT_TICKERS,
    ENV_DESTINATION_FILE_PATH,
    ENV_MAX_WORKERS,
    TIMESTAMP_FILE_SUFFIX,
)

logger = getLogger(__name__)


class Config:
    """Paths and concurrency limits for one pipeline run."""

    def __init__(self, stock_tickers: List[StockTicker], timestamps_file_path_dict: Dict[StockTicker, str], destination_file_path: str, max_workers: int):
        self._stock_tickers = stock_tickers
        self._timestamps_file_path_dict = timestamps_file_path_dict
        self._destination_file_path = destination_file_path
        self._max_workers = max_workers

    @classmethod
    def from_env(cls) -> "Config":
        """Build config for BTC, GOOGL, and AMZN.

        Timestamp files are ``{TICKER}.txt``. Destination path and worker count
        fall back to ``DEFAULT_DESTINATION_FILE_PATH`` and ``DEFAULT_MAX_WORKERS``.
        """
        load_dotenv()
        stock_tickers = [StockTicker(symbol) for symbol in DEFAULT_TICKERS]
        timestamps_file_path_dict = {
            ticker: f"{ticker.value}{TIMESTAMP_FILE_SUFFIX}" for ticker in stock_tickers
        }
        destination_file_path = os.getenv(ENV_DESTINATION_FILE_PATH, DEFAULT_DESTINATION_FILE_PATH)
        max_workers = int(os.getenv(ENV_MAX_WORKERS, str(DEFAULT_MAX_WORKERS)))
        config = cls(
            stock_tickers=stock_tickers,
            timestamps_file_path_dict=timestamps_file_path_dict,
            destination_file_path=destination_file_path,
            max_workers=max_workers,
        )
        logger.info(
            "Config loaded: tickers=%s destination=%s max_workers=%d",
            [ticker.value for ticker in stock_tickers],
            destination_file_path,
            max_workers,
        )
        return config
    @property
    def stock_tickers(self) -> list[StockTicker]:
        return self._stock_tickers

    @property
    def timestamps_file_path_dict(self) -> dict[StockTicker, str]:
        return self._timestamps_file_path_dict

    @property
    def destination_file_path(self) -> str:
        return self._destination_file_path

    @property
    def max_workers(self) -> int:
        return self._max_workers


