"""Entry point: load config from the environment and run the stock pipeline."""

import sys
import warnings
from logging import getLogger, basicConfig
from pipeline import run_pipeline
from config import Config
from constants import EXIT_CODE_FAILURE, LOG_DATE_FORMAT, LOG_FORMAT, LOG_LEVEL



basicConfig(level=LOG_LEVEL, format=LOG_FORMAT, datefmt=LOG_DATE_FORMAT)
logger = getLogger(__name__)


def main() -> None:
    """Run the pipeline. On a fatal error, log the traceback and exit 1."""
    try:
        run_pipeline(Config.from_env())
    except Exception:
        logger.exception("Pipeline failed")
        sys.exit(EXIT_CODE_FAILURE)


if __name__ == "__main__":
    logger.info("Starting main")
    main()
