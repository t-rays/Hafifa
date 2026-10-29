"""w3resource #3: restaurant_id, name, borough, cuisine; exclude _id."""

from pymongo.database import Database


def run(db: Database):
    restaurants = db["restaurants"]
    return restaurants.find({},{
        "restaurant_id": 1,
        "name": 1,
        "borough": 1,
        "cuisine": 1,
        "_id": 0,
    })
