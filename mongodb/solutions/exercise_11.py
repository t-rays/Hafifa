"""w3resource #11: not American cuisine, grade score > 70, coord value < -65.754168."""

from pymongo.database import Database


def run(db: Database):
    return list(
        db["restaurants"].find(
            {
                "cuisine": {"$ne": "American "},
                "grades.score": {"$gt": 70},
                "address.coord": {"$lt": -65.754168},
            }
        )
    )
