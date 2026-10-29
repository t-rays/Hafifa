"""w3resource #10: restaurants where address.coord is less than -95.754168 (w3resource #10)."""

from pymongo.database import Database


def run(db: Database):
    restaurants = db["restaurants"]
    return restaurants.find({"address.coord":{"$lt":-95.754168}},{"name":1,"_id":0,"address.coord":1})
