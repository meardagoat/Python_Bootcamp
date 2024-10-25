import json
import pandas as pd

def pandas_json_read(file: str) -> pd.DataFrame:
    try:
        return pd.read_json(file)
    except ValueError as e:
        print(f"Error reading JSON file: {e}")
        return pd.DataFrame()

def pandas_json_write(file: str, data: pd.DataFrame):
    try:
        data.to_json(file, indent=4, orient="records")
    except ValueError as e:
        print(f"Error writing JSON file: {e}")

def pandas_complex_json(file: str, product: dict):
    try:
        with open(file, 'r') as f:
            json_data = json.load(f)

        if len(json_data) > 0 and 'products' in json_data[0]:
            json_data[0]['products'].append(product)
        else:
            print("Error: 'products' key not found in the first element or the list is empty.")
            return pd.DataFrame()

        if len(json_data) > 1:
            del json_data[1]
        else:
            print("Error: Second element not found in the list.")
            return pd.DataFrame()

        if 'products' in json_data[1] and len(json_data[1]['products']) > 1:
            json_data[1]['products'].pop(1)
        else:
            print("Error: 'products' key not found in the second element or not enough products to pop.")
            return pd.DataFrame()

        with open(file, 'w') as f:
            json.dump(json_data, f, indent=2)

        df = pd.json_normalize(
            json_data,
            record_path=['products'],
            meta=[
                'order_id',
                ['customer', 'firstname'],
                ['customer', 'name']
            ]
        )
        return df
    except (json.JSONDecodeError, KeyError, IndexError) as e:
        print(f"Error processing JSON file: {e}")
        return pd.DataFrame()

if __name__ == "__main__":
    # Test de la fonction
    json_file = 'example.json'
    product = {
        "product_id": 4,
        "name": "Product4",
        "quantity": 40,
        "price": 400.0
    }

    df = pandas_json_read(json_file)
    if not df.empty:
        print(df)

    pandas_json_write('output.json', df)

    complex_df = pandas_complex_json(json_file, product)
    if not complex_df.empty:
        print(complex_df)