import pandas as pd

# Create a DataFrame with example data
data = {
    'product': ['Product1', 'Product2', 'Product3'],
    'quantity': [10, 20, 30],
    'total_price': [100.0, 200.0, 300.0]
}
df = pd.DataFrame(data)

# Write the DataFrame to an Excel file with a sheet named 'orders'
df.to_excel('example.xlsx', sheet_name='orders', index=False)

def pandas_excel_read(file: str, sheet: str) -> pd.DataFrame:
    try:
        return pd.read_excel(file, sheet_name=sheet)
    except FileNotFoundError:
        print(f"Error: The file {file} does not exist.")
        return pd.DataFrame()
    except ValueError:
        print(f"Error: The sheet {sheet} does not exist in the file {file}.")
        return pd.DataFrame()

def pandas_excel_write(data: pd.DataFrame, filename: str):
    try:
        sheets = pd.read_excel(filename, sheet_name=None)
    except FileNotFoundError:
        sheets = {}
    sheets["orders"] = data
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        for sheet_name, sheet_data in sheets.items():
            sheet_data.to_excel(writer, sheet_name=sheet_name, index=False)

def pandas_excel_selective_read(filename: str) -> pd.DataFrame:
    try:
        df = pd.read_excel(filename, sheet_name='orders', usecols=['product', 'total_price'], skiprows=range(1, 11))
        result = df.groupby('product')['total_price'].sum().reset_index()
        return result
    except FileNotFoundError:
        print(f"Error: The file {filename} does not exist.")
        return pd.DataFrame()
    except ValueError:
        print(f"Error: The sheet 'orders' does not exist in the file {filename}.")
        return pd.DataFrame()

def pandas_excel_manipulation(filename: str):
    try:
        data = pd.read_excel(filename, sheet_name="orders")
        summary = data.groupby(['product']).agg(
            total_orders=('product', 'size'),
            total_quantity=('quantity', 'sum')
        )
        summary['mean_quantity_per_order'] = (summary['total_quantity'] / summary['total_orders']).round(2)
        summary.reset_index(inplace=True)
        with pd.ExcelWriter(filename, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
            summary.to_excel(writer, sheet_name='summary', index=False)
    except FileNotFoundError:
        print(f"Error: The file {filename} does not exist.")
    except ValueError:
        print(f"Error: The sheet 'orders' does not exist in the file {filename}.")

if __name__ == "__main__":
    # Test de la fonction
    df = pandas_excel_read("example.xlsx", "orders")
    if not df.empty:
        print(df)

        headers = ["product", "quantity", "total_price"]
        data = [("Product1", 10, 100.0), ("Product2", 20, 200.0)]
        pandas_excel_write(pd.DataFrame(data, columns=headers), "output.xlsx")

        selective_df = pandas_excel_selective_read("output.xlsx")
        if not selective_df.empty:
            print(selective_df)

            pandas_excel_manipulation("output.xlsx")


