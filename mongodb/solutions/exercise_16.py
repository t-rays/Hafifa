"""w3resource #16: restaurant_id, name, borough, cuisine; name contains Reg."""

from pymongo.database import Database


def run(db: Database):
    return list(
        db["restaurants"].find(
            {"name": {"$regex": "Reg"}},
            {
                "_id": 0,
                "restaurant_id": 1,
                "name": 1,
                "borough": 1,
                "cuisine": 1,
            },
        )
    )
