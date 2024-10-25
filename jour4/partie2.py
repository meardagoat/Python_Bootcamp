from pymongo import MongoClient, DESCENDING, TEXT, ASCENDING
import time

def create_award_year_index(client: MongoClient):
    return client.nobel.laureates.create_index([("prizes.year", DESCENDING)])

def get_laureates_year(client: MongoClient, year: int) -> list[dict]:
    db = client['nobel']
    laureates_collection = db['laureates']
    laureates = list(laureates_collection.find({"prizes.year": year}))
    return laureates

def create_country_index(client: MongoClient):
    return client.nobel.laureates.create_index([("bornCountry", TEXT), ("diedCountry", TEXT)])

def get_country_laureates(client: MongoClient, country: str) -> list[dict]:
    try:
        laureates = list(client.nobel.laureates.find(
            {"bornCountry": country},
            {"firstname": 1, "surname": 1, "bornCountry": 1, "diedCountry": 1, "_id": 0}
        ))
        return laureates
    except Exception as e:
        print(f"Error retrieving laureates: {e}")
        return []

def create_gender_category_index(client: MongoClient) -> str:
    index_name = client["nobel"]["laureates"].create_index(
        [("prizes.category", DESCENDING), ("gender", ASCENDING)]
    )
    return index_name

def get_gender_category_laureates(client: MongoClient, gender: str, category: str) -> list[dict]:
    results = client["nobel"]["laureates"].find(
        {
            "gender": gender,
            "prizes.category": category
        },
        {
            "_id": 0,
            "firstname": 1,
            "surname": 1,
            "born": 1,
            "died": 1,
            "bornCountry": 1,
            "diedCountry": 1,
            "gender": 1,
            "prizes": {
                "$elemMatch": {
                    "category": category
                }
            }
        }
    )
    return list(results)

def create_year_category_index(client: MongoClient) -> str:
    index_name = client["nobel"]["prizes"].create_index(
        [("year", ASCENDING), ("category", ASCENDING)],
        unique=True
    )
    return index_name

# Test de la partie 2
if __name__ == "__main__":
    client = MongoClient("mongodb://localhost:27017/")
    create_award_year_index(client)
    laureates = get_laureates_year(client, 2000)
    print(f"Number of laureates in 2000: {len(laureates)}")

    create_country_index(client)
    laureates = get_country_laureates(client, "France")
    print(f"Number of laureates from France: {len(laureates)}")