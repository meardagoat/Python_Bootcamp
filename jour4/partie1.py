from pymongo import MongoClient
import re


def connect_to_mongo(host: str, port: int) -> MongoClient:
    try:
        client = MongoClient(host, port)
        return client
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        return None


def fetch_all_laureates(client: MongoClient) -> list[dict]:
    return list(client.nobel.laureates.find())


def fetch_laureates_info(client: MongoClient) -> list[dict]:
    return list(client["nobel"]["laureates"].find({}, {"_id": 0, "firstname": 1, "surname": 1, "born": 1}))


def fetch_prize_categories(client: MongoClient) -> list[str]:
    return list(client["nobel"]["prizes"].distinct("category"))


def fetch_laureates_by_category(client: MongoClient, category: str) -> list[dict]:
    return list(client.nobel.laureates.find({"prizes.category": category},
                                            {"firstname": 1, "surname": 1, "prizes.category": 1, "_id": 0}))


def fetch_laureates_by_country(client: MongoClient, country: str) -> list[dict]:
    country_pattern = re.compile(f".*{re.escape(country)}.*", re.IGNORECASE)
    laureates = client.nobel.laureates.find(
        {"bornCountry": country_pattern},
        {"firstname": 1, "surname": 1, "bornCountry": 1, "_id": 0}
    )
    return list(laureates)


def fetch_shared_prizes(client: MongoClient) -> list[dict]:
    pipeline = [
        {"$unwind": "$prizes"},
        {"$group": {
            "_id": {"category": "$prizes.category", "year": "$prizes.year"},
            "count": {"$sum": 1},
            "laureates": {"$push": {"firstname": "$firstname", "surname": "$surname", "share": "$prizes.share"}}
        }},
        {"$match": {"count": {"$gt": 1}}},
        {"$project": {
            "_id": 0,
            "category": "$_id.category",
            "year": "$_id.year",
            "laureates": 1
        }}
    ]
    shared_prizes = client.nobel.laureates.aggregate(pipeline)
    return list(shared_prizes)


def fetch_sorted_laureates_info(client: MongoClient) -> list[dict]:
    laureates = client.nobel.laureates.find(
        {},
        {"firstname": 1, "surname": 1, "bornCountry": 1, "born": 1, "_id": 0}
    ).sort([
        ("bornCountry", -1),
        ("born", 1)
    ])
    return list(laureates)

# Test de la partie 1
if __name__ == "__main__":
    client = connect_to_mongo("localhost", 27017)
    if client:
        print("All Laureates:")
        print(fetch_all_laureates(client))

        print("\nLaureates Info:")
        print(fetch_laureates_info(client))

        print("\nPrize Categories:")
        print(fetch_prize_categories(client))

        print("\nLaureates by Category (e.g., 'physics'):")
        print(fetch_laureates_by_category(client, "physics"))

        print("\nLaureates by Country (e.g., 'USA'):")
        print(fetch_laureates_by_country(client, "USA"))

        print("\nShared Prizes:")
        print(fetch_shared_prizes(client))

        print("\nSorted Laureates Info:")
        print(fetch_sorted_laureates_info(client))