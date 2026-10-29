"""w3resource #10: restaurants where address.coord is less than -95.754168 (w3resource #10)."""

from pymongo.database import Database


def run(db: Database):
    return list(db["restaurants"].find({"address.coord": {"$lt": -95.754168}}))
