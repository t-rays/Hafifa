"""w3resource #12: not American, score > 70, longitude < -65.754168 (no $and)."""

from pymongo.database import Database


def run(db: Database):
    return list(
        db["restaurants"].find(
            {
                "cuisine": {"$ne": "American "},
                "grades.score": {"$gt": 70},
                "address.coord.0": {"$lt": -65.754168},
            }
        )
    )
