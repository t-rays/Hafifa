"""w3resource #6: first 5 restaurants in the borough Bronx."""

from pymongo.database import Database


def run(db: Database):
    restaurants = db["restaurants"]
    return restaurants.find({"borough":"Bronx"},{"name":1,"_id":0}).limit(5)
