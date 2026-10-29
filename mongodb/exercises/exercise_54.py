"""w3resource #54: count of restaurants in each borough."""

from pymongo.database import Database


def run(db: Database):
    restaurants = db["restaurants"]
    return list( restaurants.aggregate([{"$group":{"_id":"$borough","count":{"$sum":1}}}]))