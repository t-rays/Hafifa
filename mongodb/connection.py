"""MongoDB client for local onboarding exercises."""

import os

from pymongo import MongoClient
from pymongo.database import Database

DEFAULT_URI = "mongodb://127.0.0.1:27017"
DEFAULT_DB = "onboarding_mongodb"


def _connection_uri(explicit: str | None) -> str:
    if explicit:
        return explicit
    from_env = os.environ.get("MONGODB_URI", "").strip()
    if not from_env:
        return DEFAULT_URI
    if "USER:PASSWORD" in from_env or "CLUSTER.mongodb" in from_env:
        raise ValueError(
            "MONGODB_URI still has placeholder text. "
            "For local Homebrew Mongo, run: unset MONGODB_URI"
        )
    if from_env.startswith("mongodb+srv://") and (
        "://@" in from_env or from_env.startswith("mongodb+srv://@")
    ):
        raise ValueError(
            "MONGODB_URI Atlas string is missing username/password. "
            "Fix the URI or run: unset MONGODB_URI"
        )
    return from_env


def get_database(
    uri: str | None = None,
    db_name: str | None = None,
) -> Database:
    """Return a handle to the exercise database."""
    client = MongoClient(_connection_uri(uri))
    return client[db_name or os.environ.get("MONGO_DB", DEFAULT_DB)]
