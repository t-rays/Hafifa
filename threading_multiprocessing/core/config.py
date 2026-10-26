"""Environment-driven settings for the stock-price pipeline.

Values come from the process environment and, when present, the package ``.env``.
Relative paths are resolved against the package root.
"""

from pathlib import Path
from typing import Literal, Self

from pydantic import Field, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from core.constant import (
    DEFAULT_DESTINATION_FILE,
    DEFAULT_LOG_LEVEL,
    DEFAULT_MAX_WORKERS,
    ENV_FILE,
    PACKAGE_DIR,
    PROCESSED_DATA_DIR,
    RAW_DATA_DIR,
)


class Config(BaseSettings):
    """Runtime settings loaded from ``LOG_LEVEL``, ``OUTPUT_DIR``, ``MAX_WORKERS``,
    ``DESTINATION_FILE``, ``HOURS_DIR``, and ``*_DATES``.

    Attributes:
        destination_file: Report path. A bare filename is placed under
            ``output_dir``.
        max_workers: Concurrent Yahoo downloads; must be greater than zero.
        bitcoin_dates: Optional override for the Bitcoin hours file.
        google_dates: Optional override for the Google hours file.
        amazon_dates: Optional override for the Amazon hours file.
    """

    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_file_encoding="utf-8",
        extra="ignore",
    )

    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = DEFAULT_LOG_LEVEL
    output_dir: Path = PROCESSED_DATA_DIR
    destination_file: Path = DEFAULT_DESTINATION_FILE
    max_workers: int = Field(default=DEFAULT_MAX_WORKERS, gt=0)
    hours_dir: Path = RAW_DATA_DIR

    bitcoin_dates: Path | None = None
    google_dates: Path | None = None
    amazon_dates: Path | None = None

    @field_validator("output_dir", "hours_dir")
    @classmethod
    def _relative_to_package(cls, path: Path) -> Path:
        return path if path.is_absolute() else PACKAGE_DIR / path

    @field_validator("bitcoin_dates", "google_dates", "amazon_dates")
    @classmethod
    def _optional_relative_to_package(cls, path: Path | None) -> Path | None:
        if path is None:
            return None
        return path if path.is_absolute() else PACKAGE_DIR / path

    @model_validator(mode="after")
    def _resolve_destination_file(self) -> Self:
        """Join a bare filename to ``output_dir``; resolve other relative paths
        against the package root."""
        destination = self.destination_file
        if destination.is_absolute():
            return self
        if len(destination.parts) == 1:
            self.destination_file = self.output_dir / destination.name
        else:
            self.destination_file = PACKAGE_DIR / destination
        return self
