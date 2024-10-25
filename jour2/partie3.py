import pandas as pd
import sys
import csv

def create_series() -> pd.Series:
    values = [int(arg) for arg in sys.argv[1:]]
    return pd.Series(values)

def series_operations(series: pd.Series) -> (int, float, float):
    total = series.sum()
    average = series.mean()
    deviation = series.std()
    return total, average, deviation

def native_csv_read(file: str) -> list[tuple]:
    with open(file, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        next(reader)  # Skip header
        data = [(idx, *row) for idx, row in enumerate(reader)]
    return data

def create_dataframe(products: list[str], quantities: list[int], prices: list[float]) -> pd.DataFrame:
    return pd.DataFrame({
        'Product': products,
        'Quantity': quantities,
        'Total_Price': prices
    })

def dataframe_accession(data: pd.DataFrame) -> tuple:
    product_list = data['Product'].tolist()
    second_row_dict = data.iloc[1].to_dict()
    third_product_quantity = data.loc[2, 'Quantity']
    return product_list, second_row_dict, third_product_quantity

if __name__ == "__main__":
    # Test de la fonction
    series = create_series()
    total, average, deviation = series_operations(series)
    print(f"Total: {total}, Average: {average}, Deviation: {deviation}")

    data = native_csv_read("example.csv")
    print(data)

    products = ["Product1", "Product2", "Product3"]
    quantities = [10, 20, 30]
    prices = [100.0, 200.0, 300.0]
    df = create_dataframe(products, quantities, prices)
    print(df)

    product_list, second_row_dict, third_product_quantity = dataframe_accession(df)
    print(f"Product List: {product_list}")
    print(f"Second Row: {second_row_dict}")
    print(f"Third Product Quantity: {third_product_quantity}")