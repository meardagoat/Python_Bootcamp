from pymongo import MongoClient
from bson import ObjectId

def add_laureate(client: MongoClient, laureate: dict) -> ObjectId:
    db = client['nobel']
    collection = db['laureates']
    insertion_result = collection.insert_one(laureate)
    return insertion_result.inserted_id

def add_prizes(client: MongoClient, prizes: list[dict]) -> list[ObjectId]:
    db = client['nobel']
    collection = db['prizes']
    insertion_result = collection.insert_many(prizes)
    return insertion_result.inserted_ids

def update_laureate(client: MongoClient, doc_id: ObjectId, dod: str, country: str, city: str) -> tuple[int, int]:
    db = client['nobel']
    collection = db['laureates']
    update_result = collection.update_one(
        {"_id": doc_id},
        {"$set": {"died": dod, "diedCountry": country, "diedCity": city}}
    )
    return (update_result.matched_count, update_result.modified_count)

def upper_categories(client: MongoClient) -> tuple[int, int]:
    db = client['nobel']
    collection = db['prizes']
    update_result = collection.update_many(
        {},
        [{"$set": {"category": {"$toUpper": "$category"}}}]
    )
    return (update_result.matched_count, update_result.modified_count)

def delete_prize(client: MongoClient, prize_id: ObjectId) -> tuple[int, int]:
    db = client['nobel']
    collection = db['prizes']
    delete_result = collection.delete_one({"_id": prize_id})
    return (1 if delete_result.deleted_count > 0 else 0, delete_result.deleted_count)

def delete_laureates(client: MongoClient, dob: str) -> (int, int):
    db = client['nobel']
    collection = db['laureates']
    count_before = collection.count_documents({"born": {"$lt": dob}})
    delete_result = collection.delete_many({"born": {"$lt": dob}})
    return count_before, delete_result.deleted_count

# Test de la partie 4
if __name__ == "__main__":
    client = MongoClient()

    # Test de laureate
    laureate = {
        "firstname": "John",
        "surname": "Doe",
        "born": "2000-01-01",
        "bornCountry": "USA",
        "bornCity": "New York"
    }
    laureate_id = add_laureate(client, laureate)
    print(f"Added laureate with ID: {laureate_id}")

    # Test du add_prizes
    prizes = [
        {"year": 2021, "category": "physics", "laureates": [{"id": "1", "firstname": "John", "surname": "Doe"}]},
        {"year": 2021, "category": "chemistry", "laureates": [{"id": "2", "firstname": "Jane", "surname": "Smith"}]}
    ]
    prize_ids = add_prizes(client, prizes)
    print(f"Added prizes with IDs: {prize_ids}")

    # Test de update_laureate
    update_result = update_laureate(client, laureate_id, "2022-01-01", "USA", "New York")
    print(f"Update laureate result: {update_result}")

    # Test du upper_categories
    upper_result = upper_categories(client)
    print(f"Upper categories result: {upper_result}")

    # Test de delete_prize
    prize_id = prize_ids[0]
    delete_prize_result = delete_prize(client, prize_id)
    print(f"Delete prize result: {delete_prize_result}")

    # Test de delete_laureates
    delete_laureates_result = delete_laureates(client, "1990-01-01")
    print(f"Delete laureates result: {delete_laureates_result}")