"""w3resource #61: average score for each cuisine."""

from pymongo.database import Database


def run(db: Database):
    restaurants = db["restaurants"]
    return list( restaurants.aggregate([{"$group":{"_id":"$cuisine","average_score":{"$avg":"$grades.score"}}}]))
