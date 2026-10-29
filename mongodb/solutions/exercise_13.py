"""w3resource #13: not American, grade A, not Brooklyn; sort by cuisine descending."""

from pymongo.database import Database


def run(db: Database):
    return list(
        db["restaurants"]
        .find(
            {
                "cuisine": {"$ne": "American "},
                "grades.grade": "A",
                "borough": {"$ne": "Brooklyn"},
            },
            {
                "_id": 0,
                "restaurant_id": 1,
                "name": 1,
                "borough": 1,
                "cuisine": 1,
            },
        )
        .sort("cuisine", -1)
    )
