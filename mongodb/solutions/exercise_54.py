from pymongo.database import Database


def run(db: Database):
    pipeline = [
        {"$group": {"_id": "$borough", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
    ]
    return list(db["restaurants"].aggregate(pipeline))
