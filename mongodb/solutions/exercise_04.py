"""w3resource #4: restaurant_id, name, borough, zipcode; exclude _id."""

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
                "address.zipcode": 1,
            },
        )
    )
