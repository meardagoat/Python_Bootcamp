import pandas as pd

def pandas_csv_read(file: str) -> pd.DataFrame:
    dataframe = pd.read_csv(file)
    return dataframe

def pandas_csv_write(file: str, headers: list, data: list[tuple]):
    rows_without_index = [row[1:] for row in data]
    dataframe = pd.DataFrame(rows_without_index, columns=headers)
    dataframe.to_csv(file, index=False)

if __name__ == "__main__":
    # Test de la fonction
    df = pandas_csv_read("example.csv")
    print(df)

    headers = ["Column1", "Column2"]
    data = [(0, "value1", "value2"), (1, "value3", "value4")]
    pandas_csv_write("output.csv", headers, data)