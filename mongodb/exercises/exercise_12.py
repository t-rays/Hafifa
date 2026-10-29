"""w3resource #12: not American, score > 70, longitude < -65.754168 (no $and)."""

from pymongo.database import Database


def run(db: Database):
    restaurants = db["restaurants"]
    # TODO: query and return results (list or cursor)
    raise NotImplementedError
