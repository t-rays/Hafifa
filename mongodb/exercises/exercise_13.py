"""w3resource #13: not American, grade A, not Brooklyn; sort by cuisine descending."""

from pymongo.database import Database


def run(db: Database):
    restaurants = db["restaurants"]
    return restaurants.find({"cuisine":{"$ne":"American"},"grades.grade":"A","borough":{"$ne":"Brooklyn"}},{"name":1,"_id":0,"cuisine":1}).sort("cuisine",-1)
