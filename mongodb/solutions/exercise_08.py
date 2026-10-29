"""w3resource #8: restaurants that achieved a score more than 90."""

from pymongo.database import Database


def run(db: Database):
    return list(
        db["restaurants"].find(
            {"grades": {"$elemMatch": {"score": {"$gt": 90}}}}
        )
    )
