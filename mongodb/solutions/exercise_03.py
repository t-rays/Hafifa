"""w3resource #3: restaurant_id, name, borough, cuisine; exclude _id."""

from pymongo.database import Database


def run(db: Database):
    return list(
        db["restaurants"].find(
            {},
            {
                "_id": 0,
                "restaurant_id": 1,
                "name": 1,
                "borough": 1,
                "cuisine": 1,
            },
        )
    )
