"""w3resource #7: next 5 Bronx restaurants after skipping the first 5."""

from pymongo.database import Database


def run(db: Database):
    return list(db["restaurants"].find({"borough": "Bronx"}).skip(5).limit(5))
