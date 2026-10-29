"""w3resource #19: restaurant_id, name, borough, cuisine; borough not in SI, Queens, Bronx, Brooklyn."""

from pymongo.database import Database


def run(db: Database):
    return list(
        db["restaurants"].find(
            {
                "borough": {
                    "$nin": ["Staten Island", "Queens", "Bronx", "Brooklyn"]
                }
            },
            {
                "_id": 0,
                "restaurant_id": 1,
                "name": 1,
                "borough": 1,
                "cuisine": 1,
            },
        )
    )
