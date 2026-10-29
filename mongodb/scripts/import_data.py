#!/usr/bin/env python3
"""Download (if needed) and load w3resource restaurants.json via PyMongo."""

from __future__ import annotations

import json
import os
import sys
import zipfile
from pathlib import Path
from urllib.request import urlretrieve

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
JSON_PATH = DATA_DIR / "restaurants.json"
ZIP_URL = "https://www.w3resource.com/mongodb-exercises/restaurants.zip"
BATCH = 500


def download_dataset() -> Path:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if JSON_PATH.is_file():
        return JSON_PATH
    zip_path = DATA_DIR / "restaurants.zip"
    print(f"Downloading {ZIP_URL} ...")
    urlretrieve(ZIP_URL, zip_path)
    with zipfile.ZipFile(zip_path) as zf:
        zf.extractall(DATA_DIR)
    zip_path.unlink(missing_ok=True)
    if not JSON_PATH.is_file():
        raise FileNotFoundError(f"Expected {JSON_PATH} after unzip")
    return JSON_PATH


def load_into_mongo(json_path: Path) -> int:
    sys.path.insert(0, str(ROOT))
    from connection import get_database

    db_name = os.environ.get("MONGO_DB", "onboarding_mongodb")
    collection_name = os.environ.get("MONGO_COLLECTION", "restaurants")
    db = get_database()
    coll = db[collection_name]
    coll.drop()

    total = 0
    batch: list[dict] = []
    with json_path.open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            batch.append(json.loads(line))
            if len(batch) >= BATCH:
                coll.insert_many(batch)
                total += len(batch)
                batch.clear()
    if batch:
        coll.insert_many(batch)
        total += len(batch)

    print(f"Imported {total} documents into {db_name}.{collection_name}")
    return total


def main() -> None:
    only_download = "--download-only" in sys.argv
    path = download_dataset()
    if only_download:
        print(f"Dataset ready at {path}")
        return
    load_into_mongo(path)


if __name__ == "__main__":
    main()
