"""w3resource #18: restaurant_id, name, borough, cuisine; Staten Island, Queens, Bronx, or Brooklyn."""

from pymongo.database import Database


def run(db: Database):
    restaurants = db["restaurants"]
    return restaurants.find({"borough":{"$in":["Staten Island","Queens","Bronx","Brooklyn"]}},{"restaurant_id":1,"name":1,"borough":1,"cuisine":1,"_id":0})
