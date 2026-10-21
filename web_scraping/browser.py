"""Async URL scraper using Playwright (Chromium).

Reads URLs from ``input/urls.input``, visits each page concurrently (bounded
by ``MAX_CONCURRENT_TASKS``), and writes per-URL artifacts under ``output/``:

  ``output/url_<n>/screenshot.png``
  ``output/url_<n>/browse.json`` — keys ``html``, ``resources``, ``screenshot``

Run from this directory::

    python browser.py

Requires Playwright Chromium: ``playwright install chromium``.
"""

import asyncio
import base64
import json
import logging
from pathlib import Path

from playwright.async_api import async_playwright, BrowserContext

from constants import (
    BROWSE_JSON_FILENAME,
    BROWSER_HEADLESS,
    BROWSER_LAUNCH_ARGS,
    FILE_ENCODING,
    INPUT_FILE,
    JSON_INDENT,
    LOG_DATE_FORMAT,
    LOG_FORMAT,
    MAX_CONCURRENT_TASKS,
    OUTPUT_DIR,
    PAGE_GOTO_TIMEOUT_MS,
    PAGE_GOTO_WAIT_UNTIL,
    SCREENSHOT_FILENAME,
    SCREENSHOT_FULL_PAGE,
    URL_FOLDER_PREFIX,
    URL_INDEX_START,
    USER_AGENT,
    VIEWPORT_HEIGHT,
    VIEWPORT_WIDTH,
)

logger = logging.getLogger(__name__)


def read_urls(file_path: Path) -> list[str]:
    """Load trimmed, non-empty lines from the URL input file.

    Args:
        file_path: Path to the newline-delimited URL list (typically
            ``input/urls.input``).

    Returns:
        URLs in file order. Empty list if the file is missing or has no
        non-blank lines (a warning is logged when the file does not exist).
    """
    if not file_path.exists():
        logger.warning("%s does not exist.", file_path)
        return []
    with file_path.open("r", encoding=FILE_ENCODING) as f:
        return [line.strip() for line in f if line.strip()]


async def process_url(
    context: BrowserContext,
    url: str,
    index: int,
    semaphore: asyncio.Semaphore,
) -> None:
    """Visit one URL and write ``browse.json`` plus ``screenshot.png``.

    Uses a dedicated page on the shared browser context. Network ``request``
    events are collected into ``resources`` (every requested URL during the
    visit, including the document and subresources).

    Args:
        context: Shared Playwright browser context (viewport and user agent
            are configured in ``main``).
        url: Target page URL.
        index: 1-based folder index (``output/url_<index>/``).
        semaphore: Limits how many pages load at once.

    Side effects:
        Creates ``output/url_<index>/`` on success or partial failure.
        Logs and skips JSON write if navigation or capture raises; the page
        is always closed in ``finally``.
    """
    async with semaphore:
        target_dir = OUTPUT_DIR / f"{URL_FOLDER_PREFIX}{index}"
        target_dir.mkdir(parents=True, exist_ok=True)

        screenshot_path = target_dir / SCREENSHOT_FILENAME
        json_path = target_dir / BROWSE_JSON_FILENAME

        page = await context.new_page()
        loaded_resources: list[str] = []

        page.on("request", lambda req: loaded_resources.append(req.url))

        logger.info("[%s] Navigating to: %s", index, url)
        try:
            await page.goto(
                url,
                wait_until=PAGE_GOTO_WAIT_UNTIL,
                timeout=PAGE_GOTO_TIMEOUT_MS,
            )

            html_content = await page.content()

            screenshot_bytes = await page.screenshot(
                path=str(screenshot_path),
                full_page=SCREENSHOT_FULL_PAGE,
            )

            screenshot_base64 = base64.b64encode(screenshot_bytes).decode(FILE_ENCODING)

            payload = {
                "html": html_content,
                "resources": loaded_resources,
                "screenshot": screenshot_base64,
            }

            with json_path.open("w", encoding=FILE_ENCODING) as f:
                json.dump(payload, f, indent=JSON_INDENT, ensure_ascii=False)

            logger.info("[%s] Successfully processed: %s", index, url)

        except Exception:
            logger.exception("[%s] Failed processing %s", index, url)
        finally:
            await page.close()


async def main() -> None:
    """Orchestrate scraping: read URLs, launch Chromium, run tasks in parallel.

    Exits early when there are no URLs. One browser context is shared across
    tasks; concurrency is capped by ``MAX_CONCURRENT_TASKS``.
    """
    urls = read_urls(INPUT_FILE)
    if not urls:
        logger.warning("No URLs found to process.")
        return

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    semaphore = asyncio.Semaphore(MAX_CONCURRENT_TASKS)

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=BROWSER_HEADLESS,
            args=list(BROWSER_LAUNCH_ARGS),
        )
        context = await browser.new_context(
            viewport={"width": VIEWPORT_WIDTH, "height": VIEWPORT_HEIGHT},
            user_agent=USER_AGENT,
        )

        tasks = [
            process_url(context, url, idx, semaphore)
            for idx, url in enumerate(urls, start=URL_INDEX_START)
        ]
        await asyncio.gather(*tasks)

        await context.close()
        await browser.close()


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format=LOG_FORMAT,
        datefmt=LOG_DATE_FORMAT,
    )
    asyncio.run(main())
