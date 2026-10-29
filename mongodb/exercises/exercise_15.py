"""w3resource #15: restaurant_id, name, borough, cuisine; name ends with ces."""

from pymongo.database import Database


def run(db: Database):
    restaurants = db["restaurants"]
    return restaurants.find({"name":{"$regex":"ces$"}},{"restaurant_id":1,"name":1,"borough":1,"cuisine":1,"_id":0})
