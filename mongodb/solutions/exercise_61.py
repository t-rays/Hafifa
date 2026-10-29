from pymongo.database import Database


def run(db: Database):
    pipeline = [
        {"$unwind": "$grades"},
        {
            "$group": {
                "_id": "$cuisine",
                "avgScore": {"$avg": "$grades.score"},
            }
        },
        {"$sort": {"avgScore": -1}},
    ]
    return list(db["restaurants"].aggregate(pipeline))
