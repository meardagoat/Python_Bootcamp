import pandas as pd
import numpy as np
from jour2.partie7 import add_columns  # Import the add_columns function

def static_suppression(data: pd.DataFrame) -> pd.DataFrame:
    data = data.drop(columns=['total_price'])
    max_index = data.index.max()
    indices_to_drop = [i for i in range(5, 13) if i <= max_index]
    data = data.drop(index=indices_to_drop)
    return data.reset_index(drop=True)

def missing_data_suppression(data: pd.DataFrame) -> pd.DataFrame:
    data = data.dropna(subset=['total_price'])
    return data.reset_index(drop=True)

def duplicate_data_suppression(data: pd.DataFrame) -> pd.DataFrame:
    data = data.drop_duplicates()
    return data.reset_index(drop=True)

def number_uniformisation(data: pd.DataFrame) -> pd.DataFrame:
    data['quantity'] = data['quantity'].astype(int)
    data['total_price'] = data['total_price'].astype(float).round(2)
    return data

def string_uniformisation(data: pd.DataFrame) -> pd.DataFrame:
    data['product'] = data['product'].str.lower()
    return data

def number_validation(data: pd.DataFrame) -> bool:
    valid_price = (data['total_price'] > 0).all()
    valid_quantity = ((data['quantity'] >= 1) & (data['quantity'] <= 10)).all()
    return valid_price and valid_quantity

def enum_validation(data: pd.DataFrame, valid_products: list) -> pd.DataFrame:
    invalid_entries = data[~data['product'].isin(valid_products)]
    return invalid_entries

def cross_column_validation(data: pd.DataFrame) -> pd.DataFrame:
    invalid_rows = data[data['unit_price'] > data['montant']]
    return invalid_rows

# Test de la dataframe
def main():
    data = {
        'product': ['apple', 'banana', 'apple', 'banana', 'apple'],
        'quantity': [10, 5, 8, 7, 6],
        'total_price': [20.0, 10.0, 16.0, 14.0, 12.0],
        'montant': [20.0, 10.0, 16.0, 14.0, 12.0],
        'quantité': [10, 5, 8, 7, 6]
    }
    df = pd.DataFrame(data)
    suppressed_df = static_suppression(df)
    print("Static Suppression:")
    print(suppressed_df)

    missing_suppressed_df = missing_data_suppression(df)
    print("\nMissing Data Suppression:")
    print(missing_suppressed_df)

    duplicate_suppressed_df = duplicate_data_suppression(df)
    print("\nDuplicate Data Suppression:")
    print(duplicate_suppressed_df)

    uniformed_numbers_df = number_uniformisation(df)
    print("\nNumber Uniformisation:")
    print(uniformed_numbers_df)

    uniformed_strings_df = string_uniformisation(df)
    print("\nString Uniformisation:")
    print(uniformed_strings_df)

    is_valid_numbers = number_validation(df)
    print("\nNumber Validation:")
    print(is_valid_numbers)

    valid_products = ['apple', 'banana']
    invalid_entries = enum_validation(df, valid_products)
    print("\nEnum Validation:")
    print(invalid_entries)

    df_with_columns = add_columns(df)
    invalid_cross_rows = cross_column_validation(df_with_columns)
    print("\nCross Column Validation:")
    print(invalid_cross_rows)

if __name__ == "__main__":
    main()