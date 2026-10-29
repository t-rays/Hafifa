"""w3resource #9: restaurants with a grade score more than 80 and less than 100."""

from pymongo.database import Database


def run(db: Database):
    return list(
        db["restaurants"].find(
            {"grades": {"$elemMatch": {"score": {"$gt": 80, "$lt": 100}}}}
        )
    )
