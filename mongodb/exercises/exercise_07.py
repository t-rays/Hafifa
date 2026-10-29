"""w3resource #7: next 5 Bronx restaurants after skipping the first 5."""

from pymongo.database import Database


def run(db: Database):
    restaurants = db["restaurants"]
    return restaurants.find({"borough":"Bronx"},{"name":1,"_id":0}).skip(5).limit(5)
