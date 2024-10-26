import pandas as pd
import numpy as np


def sort_dataframe_simple(dataframe: pd.DataFrame) -> pd.DataFrame:
    return dataframe.sort_values(by='product', ascending=False).reset_index(drop=True)

def sort_dataframe_advanced(dataframe: pd.DataFrame) -> pd.DataFrame:
    return dataframe.sort_values(by=['quantity', 'total_price', 'product'],
                                 ascending=[True, False, True]).reset_index(drop=True)


def add_columns(dataframe: pd.DataFrame) -> pd.DataFrame:
    dataframe['order_number'] = ((dataframe.index + 1) % 100000).astype(str).str.zfill(5)
    dataframe['unit_price'] = (dataframe['montant'] / dataframe['quantité']).round(2)
    return dataframe

def filter_dataframe_simple(dataframe: pd.DataFrame, product_name: str) -> pd.DataFrame:
    return dataframe[(dataframe['product'] == product_name) & (dataframe['quantity'] >= 5)]

def filter_dataframe_advanced(dataframe: pd.DataFrame) -> pd.DataFrame:
    filtered_df = dataframe[(dataframe['order_number'].str[0] == '1') &
                            (dataframe['unit_price'].between(0, 2, inclusive='both'))]
    return filtered_df.sort_values(by='product').reset_index(drop=True)


def dataframe_operations(dataframe: pd.DataFrame) -> tuple:
    total_amount = round(dataframe['montant'].sum(), 2)
    total_quantity = dataframe['quantité'].sum()
    avg_price = round(dataframe['montant'].mean(), 2)
    max_amount = round(dataframe['montant'].max(), 2)
    min_amount = round(dataframe['montant'].min(), 2)
    return (total_amount, total_quantity, avg_price, max_amount, min_amount)


#Test de la dataframe
def main():

    data = {
        'product': ['apple', 'banana', 'apple', 'banana', 'apple'],
        'quantity': [10, 5, 8, 7, 6],
        'total_price': [20.0, 10.0, 16.0, 14.0, 12.0],
        'montant': [20.0, 10.0, 16.0, 14.0, 12.0],
        'quantité': [10, 5, 8, 7, 6]
    }
    df = pd.DataFrame(data)

    # Call functions and print results
    sorted_df_simple = sort_dataframe_simple(df)
    print("Sorted DataFrame (Simple):")
    print(sorted_df_simple)

    sorted_df_advanced = sort_dataframe_advanced(df)
    print("\nSorted DataFrame (Advanced):")
    print(sorted_df_advanced)

    df_with_columns = add_columns(df)
    print("\nDataFrame with Added Columns:")
    print(df_with_columns)

    filtered_df_simple = filter_dataframe_simple(df, 'apple')
    print("\nFiltered DataFrame (Simple):")
    print(filtered_df_simple)

    filtered_df_advanced = filter_dataframe_advanced(df_with_columns)
    print("\nFiltered DataFrame (Advanced):")
    print(filtered_df_advanced)

    operations_result = dataframe_operations(df)
    print("\nDataFrame Operations Result:")
    print(operations_result)

if __name__ == "__main__":
    main()