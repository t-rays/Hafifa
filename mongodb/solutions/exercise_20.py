"""w3resource #20: restaurant_id, name, borough, cuisine; at least one grade score not more than 10."""

from pymongo.database import Database


def run(db: Database):
    return list(
        db["restaurants"].find(
            {"grades.score": {"$lte": 10}},
            {
                "_id": 0,
                "restaurant_id": 1,
                "name": 1,
                "borough": 1,
                "cuisine": 1,
            },
        )
    )
