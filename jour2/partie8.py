import pandas as pd
import numpy as np


def static_suppression(df: pd.DataFrame) -> pd.DataFrame:
    df = df.drop(columns=['total_price'])
    df = df.drop(index=range(5, 13))
    return df.reset_index(drop=True)

def missing_data_suppression(df: pd.DataFrame) -> pd.DataFrame:
    df = df.dropna(subset=['price'])
    return df.reset_index(drop=True)

def duplicate_data_suppression(df: pd.DataFrame) -> pd.DataFrame:
    df = df.drop_duplicates()
    return df.reset_index(drop=True)


def number_uniformisation(df: pd.DataFrame) -> pd.DataFrame:
    df['quantity'] = df['quantity'].astype(int)
    df['total_price'] = df['total_price'].astype(float).round(2)
    return df

def string_uniformisation(df: pd.DataFrame) -> pd.DataFrame:
    df['product'] = df['product'].str.lower()
    return df


def number_validation(df: pd.DataFrame) -> bool:
    price_valid = (df['total_price'] > 0).all()
    quantity_valid = ((df['quantity'] >= 1) & (df['quantity'] <= 10)).all()
    return price_valid and quantity_valid


def enum_validation(df: pd.DataFrame, products: list) -> pd.DataFrame:
    invalid_products = df[~df['product'].isin(products)]
    return invalid_products


def cross_column_validation(df: pd.DataFrame) -> pd.DataFrame:
    invalid_rows = df[df['unit_price'] > df['montant']]
    return invalid_rows