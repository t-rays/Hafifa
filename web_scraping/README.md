# Python Scraping Exercise

Write a script named `browser.py` that reads an input file called `urls.input` (located in the `input` folder), which contains different URLs separated by new lines. An example of the content of `urls.input`:

http://www.bbc.com/    
http://www.google.com/    
http://www.yahoo.com/    


The file can contain between 0 and *n* URLs (*n* is a finite number).

Your script should create an `output` directory. Inside `output`, there should be separate folders for each URL. The folder names can be `url_1`, `url_2`, ..., `url_n`. Each folder should contain a `browse.json` file, the content of which will be described later.

For each URL, you need to perform the following four tasks:

1. **HTML Content**: Extract all the HTML content of the page (as a string). This should be saved in the `json` file under the key `"html"`.
2. **Page Resources**: List all URLs that were loaded during the page load (such as images, external links, etc.). This list should be saved in the `json` file under the key `"resources"`.
3. **Page Screenshot**: Take a screenshot of the first page and save it in the directory as `screenshot.png`.
4. **Base64 Encoded Image**: Convert the saved screenshot to a base64 encoded string and store it in the `json` file under the key `"screenshot"`.

By the end, you should have the main directory containing `browser.py`, an `input` directory with `urls.input`, and an `output` directory.

In the `output` directory, you should have as many subdirectories as there are URLs in `urls.input`, with each containing `screenshot.png` and a `browse.json` file with the keys `html`, `resources`, and `screenshot`.

## Notes:
- Use Chrome as the main browser.
- It is recommended (but not mandatory for this exercise) to write tests.
- Important: Ensure efficient runtime by considering asynchronous and parallel processing.

## Implementation (this repo)

| File | Role |
|------|------|
| `browser.py` | Entry point: read URLs, async Playwright scrape, write output |
| `constants.py` | Paths, concurrency, timeouts, viewport, logging format |

### Run

From `web_scraping/` (with Playwright installed):

```bash
python browser.py
```

Install browser binaries once: `playwright install chromium`.

For editor type checking, use the venv in this folder (`web_scraping/.venv`) as the Python interpreter; `pyrightconfig.json` here points Pyright/Pylance at that environment.

### Output layout

For each line in `input/urls.input`, the script creates `output/url_<n>/` with:

- `screenshot.png` — first viewport screenshot after `load`
- `browse.json` — `html` (full page source), `resources` (request URLs seen during the visit), `screenshot` (base64 PNG)

### Documentation

Module and function docstrings in `browser.py` and `constants.py` describe behavior, arguments, and failure handling (e.g. missing input file, per-URL errors logged without stopping other tasks).
