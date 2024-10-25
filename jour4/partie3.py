from pymongo import MongoClient

def prizes_per_category_basic(client: MongoClient) -> list[dict]:
    database = client['nobel']
    collection = database['prizes']

    pipeline = [
        {"$group": {"_id": "$category", "total_prizes": {"$sum": 1}}},
    ]

    results = list(collection.aggregate(pipeline))
    return results

def prizes_per_category_sorted(client: MongoClient) -> list[dict]:
    database = client['nobel']
    collection = database['prizes']

    pipeline = [
        {"$group": {"_id": "$category", "total_prizes": {"$sum": 1}}},
        {"$sort": {"total_prizes": -1, "_id": 1}}
    ]

    results = list(collection.aggregate(pipeline))
    return results

def prizes_per_category_filtered(client: MongoClient, nb_laureates: int) -> list[dict]:
    database = client['nobel']
    collection = database['prizes']

    pipeline = [
        {"$match": {"laureates": {"$size": nb_laureates}}},
        {"$group": {"_id": "$category", "total_prizes": {"$sum": 1}}},
    ]

    results = list(collection.aggregate(pipeline))
    return results

def prizes_per_category(client: MongoClient, nb_laureates: int) -> list[dict]:
    database = client['nobel']
    collection = database['prizes']

    pipeline = [
        {"$match": {"laureates": {"$size": nb_laureates}}},
        {"$group": {"_id": "$category", "total_prizes": {"$sum": 1}}},
        {"$sort": {"total_prizes": -1, "_id": 1}}
    ]

    results = list(collection.aggregate(pipeline))
    return results

def laureates_per_birth_country_complex(client: MongoClient) -> list[dict]:
    database = client['nobel']
    collection = database['laureates']

    pipeline = [
        {"$match": {
            "$or": [
                {"died": "0000-00-00"},
                {"$expr": {"$eq": ["$bornCountry", "$diedCountry"]}}
            ]
        }},
        {"$group": {"_id": "$bornCountry", "total_laureates": {"$sum": 1}}},
        {"$sort": {"_id": 1}}
    ]

    results = list(collection.aggregate(pipeline))
    return results

# Test de la partie 3
if __name__ == "__main__":
    client = MongoClient()
    print(prizes_per_category_basic(client))
    print(prizes_per_category_sorted(client))
    print(prizes_per_category_filtered(client, 3))
    print(prizes_per_category(client, 3))
    print(laureates_per_birth_country_complex(client))