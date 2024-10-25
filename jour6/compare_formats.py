import pandas as pd
import pyarrow.parquet as pq
import time


def measure_time(func):
    start_time = time.time()
    result = func()
    end_time = time.time()
    return result, end_time - start_time


def load_csv(filename):
    return pd.read_csv(filename)


def load_parquet(filename):
    return pd.read_parquet(filename)


def load_parquet_columns(filename, columns):
    return pd.read_parquet(filename, columns=columns)
