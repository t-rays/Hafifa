"""w3resource #19: restaurant_id, name, borough, cuisine; borough not in SI, Queens, Bronx, Brooklyn."""

from pymongo.database import Database


def run(db: Database):
    restaurants = db["restaurants"]
    # TODO: query and return results (list or cursor)
    raise NotImplementedError
