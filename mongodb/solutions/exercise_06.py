"""w3resource #6: first 5 restaurants in the borough Bronx."""

from pymongo.database import Database


def run(db: Database):
    return list(db["restaurants"].find({"borough": "Bronx"}).limit(5))
