"""w3resource #17: Bronx restaurants with American or Chinese cuisine."""

from pymongo.database import Database


def run(db: Database):
    return list(
        db["restaurants"].find(
            {
                "borough": "Bronx",
                "cuisine": {"$in": ["American ", "Chinese"]},
            }
        )
    )
