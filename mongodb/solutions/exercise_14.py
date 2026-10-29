"""w3resource #14: restaurant_id, name, borough, cuisine; name starts with Wil."""

from pymongo.database import Database


def run(db: Database):
    return list(
        db["restaurants"].find(
            {"name": {"$regex": "^Wil"}},
            {
                "_id": 0,
                "restaurant_id": 1,
                "name": 1,
                "borough": 1,
                "cuisine": 1,
            },
        )
    )
