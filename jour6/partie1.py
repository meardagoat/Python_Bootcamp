import pandas as pd
import pyarrow.parquet as pq
import time


def read_parquet(filename: str) -> pd.DataFrame:
    """
    Lit un fichier parquet et retourne un DataFrame avec les 10 premières lignes.
    """
    dataframe = pd.read_parquet(filename)
    return dataframe.head(10)


def read_parquet_columns(filename: str, columns: list) -> pd.DataFrame:
    """
    Lit un fichier parquet et retourne un DataFrame avec les colonnes spécifiées.
    """
    dataframe = pd.read_parquet(filename, columns=columns)
    return dataframe


def read_parquet_batch(filename: str, batch_size: int) -> pd.DataFrame:
    """
    Lit un fichier parquet par lots et retourne un DataFrame avec les premières lignes de chaque lot.
    """
    parquet_file = pq.ParquetFile(filename)
    rows = []
    for batch in parquet_file.iter_batches(batch_size=batch_size):
        batch_df = batch.to_pandas()
        rows.extend(batch_df.head(2).values.tolist())
    result_dataframe = pd.DataFrame(rows, columns=parquet_file.schema.names)
    result_dataframe.reset_index(drop=True, inplace=True)
    return result_dataframe

#Test de la partie 1
if __name__ == "__main__":
    filename = "/Users/kyrie/PycharmProjects/jour6/flights.parquet"

    # Lire les 10 premières lignes du fichier parquet
    df_head = read_parquet(filename)
    print("Les 10 premières lignes du fichier parquet:")
    print(df_head)

    # Lire des colonnes spécifiques du fichier parquet
    columns = ["FL_DATE", "DEP_DELAY"]
    df_columns = read_parquet_columns(filename, columns)
    print("\nColonnes spécifiées du fichier parquet:")
    print(df_columns)

    # Lire le fichier parquet par lots
    batch_size = 100
    df_batch = read_parquet_batch(filename, batch_size)
    print("\nLignes des premiers lots du fichier parquet:")
    print(df_batch)
