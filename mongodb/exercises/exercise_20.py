"""w3resource #20: restaurant_id, name, borough, cuisine; at least one grade score not more than 10."""

from pymongo.database import Database


def run(db: Database):
    restaurants = db["restaurants"]
    return restaurants.find({"grades.score":{"$not":{"$gt":10}}},{"restaurant_id":1,"name":1,"borough":1,"cuisine":1,"_id":0})
