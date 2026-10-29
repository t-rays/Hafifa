"""w3resource #2: restaurant_id, name, borough, cuisine for all documents."""

from pymongo.database import Database


def run(db: Database):
    return list(
        db["restaurants"].find(
            {},
            {
                "_id": 1,
                "restaurant_id": 1,
                "name": 1,
                "borough": 1,
                "cuisine": 1,
            },
        )
    )
