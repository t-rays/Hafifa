"""w3resource #5: all restaurants in the borough Bronx."""

from pymongo.database import Database


def run(db: Database):
    return list(db["restaurants"].find({"borough": "Bronx"}))
