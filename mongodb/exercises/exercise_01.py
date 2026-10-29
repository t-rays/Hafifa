"""w3resource #1: display all documents in restaurants."""

from pymongo.database import Database


def run(db: Database):
    restaurants = db["restaurants"]
    return restaurants.find({},{})
