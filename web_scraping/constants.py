"""Paths, browser defaults, and tuning knobs for ``browser.py``.

Centralizing values here keeps ``browser.py`` focused on orchestration and
makes timeouts, concurrency, and output layout easy to adjust.
"""

from pathlib import Path

# --- Input / output layout ---
INPUT_FILE = Path("input/urls.input")
OUTPUT_DIR = Path("output")

URL_FOLDER_PREFIX = "url_"
URL_INDEX_START = 1

SCREENSHOT_FILENAME = "screenshot.png"
BROWSE_JSON_FILENAME = "browse.json"

# --- Concurrency ---
MAX_CONCURRENT_TASKS = 3

# --- Navigation and capture ---
PAGE_GOTO_TIMEOUT_MS = 45_000
PAGE_GOTO_WAIT_UNTIL = "load"
SCREENSHOT_FULL_PAGE = False

# --- Serialization ---
JSON_INDENT = 2
FILE_ENCODING = "utf-8"

# --- Browser fingerprint ---
VIEWPORT_WIDTH = 1280
VIEWPORT_HEIGHT = 800

BROWSER_HEADLESS = True
BROWSER_LAUNCH_ARGS = ("--disable-dev-shm-usage", "--no-sandbox")

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/124.0.0.0 Safari/537.36"
)

# --- Logging (``__main__`` block in browser.py) ---
LOG_FORMAT = "%(asctime)s %(levelname)s [%(name)s] %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
