"""w3resource #18: restaurant_id, name, borough, cuisine; Staten Island, Queens, Bronx, or Brooklyn."""

from pymongo.database import Database


def run(db: Database):
    return list(
        db["restaurants"].find(
            {"borough": {"$in": ["Staten Island", "Queens", "Bronx", "Brooklyn"]}},
            {
                "_id": 0,
                "restaurant_id": 1,
                "name": 1,
                "borough": 1,
                "cuisine": 1,
            },
        )
    )
