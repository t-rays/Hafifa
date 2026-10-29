"""w3resource #15: restaurant_id, name, borough, cuisine; name ends with ces."""

from pymongo.database import Database


def run(db: Database):
    return list(
        db["restaurants"].find(
            {"name": {"$regex": "ces$"}},
            {
                "_id": 0,
                "restaurant_id": 1,
                "name": 1,
                "borough": 1,
                "cuisine": 1,
            },
        )
    )
