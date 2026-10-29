"""w3resource #9: restaurants with a grade score more than 80 and less than 100."""

from pymongo.database import Database


def run(db: Database):
    restaurants = db["restaurants"]
    return restaurants.find({"grades.score":{"$gt":80,"$lt":100}},{"name":1,"_id":0,"grades.score":1})
