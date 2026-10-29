"""w3resource #17: Bronx restaurants with American or Chinese cuisine."""

from pymongo.database import Database


def run(db: Database):
    restaurants = db["restaurants"]
    return restaurants.find({"borough":"Bronx","cuisine":{"$in":["American","Chinese"]}},{"restaurant_id":1,"name":1,"borough":1,"cuisine":1,"_id":0})
