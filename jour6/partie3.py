import pandas as pd
from datetime import datetime
import numpy as np

def impute_region(df: pd.DataFrame) -> pd.DataFrame:
    region_mapping = df.groupby('country')['region'].apply(lambda x: x.mode().iloc[0]).to_dict()
    df = df.dropna(subset=['country'])
    df['region'] = df['region'].fillna(df['country'].map(region_mapping))
    df.reset_index(drop=True, inplace=True)
    return df

def impute_quantity(df: pd.DataFrame) -> pd.DataFrame:
    df['quantity'] = df['quantity'].fillna(df['quantity'].mean())
    return df

def impute_category(df: pd.DataFrame) -> pd.DataFrame:
    most_common_category = df['category'].mode().iloc[0]
    df['category'] = df['category'].fillna(most_common_category)
    return df

def handle_inconsistent_dealsize(df: pd.DataFrame) -> pd.DataFrame:
    dealsize_corrections = {
        's': 'S', 'small': 'S', '1': 'S',
        'm': 'M', 'medium': 'M', '2': 'M',
        'l': 'L', 'large': 'L', '3': 'L'
    }
    df['dealsize'] = df['dealsize'].str.lower().map(dealsize_corrections).fillna('M')
    return df

def handle_inconsistent_dates(df: pd.DataFrame) -> pd.DataFrame:
    def parse_date(date_str):
        date_formats = ['%Y-%m-%d %H:%M:%S', '%d/%m/%Y', '%m/%d/%Y', '%Y/%m/%d']
        for fmt in date_formats:
            try:
                return pd.to_datetime(date_str, format=fmt)
            except ValueError:
                continue
        return pd.NaT

    df['date'] = df['date'].apply(parse_date)
    return df

def retrieve_quantity_outliers(df: pd.DataFrame) -> pd.DataFrame:
    Q1, Q3 = df['quantity'].quantile([0.25, 0.75])
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    outliers = df[(df['quantity'] < lower_bound) | (df['quantity'] > upper_bound)]
    return outliers.sort_values('quantity')

def handle_unit_price_outliers(df: pd.DataFrame) -> pd.DataFrame:
    Q1, Q3 = df['unit_price'].quantile([0.25, 0.75])
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    df = df[df['unit_price'] >= lower_bound]
    df.loc[df['unit_price'] > upper_bound, 'unit_price'] = upper_bound
    return df.sort_values('unit_price')

def normalize_total_price(df: pd.DataFrame) -> pd.DataFrame:
    df['total_price'] = np.log(df['total_price']).round(10)
    return df

def normalize_quantity(df: pd.DataFrame) -> pd.DataFrame:
    df['quantity'] = ((df['quantity'] - df['quantity'].mean()) / df['quantity'].std()).round(10)
    return df

def normalize_unit_price(df: pd.DataFrame) -> pd.DataFrame:
    min_price, max_price = df['unit_price'].min(), df['unit_price'].max()
    df['unit_price'] = ((df['unit_price'] - min_price) / (max_price - min_price)).round(10)
    return df

# Test de la partie 3
if __name__ == "__main__":
    data = {
        'country': ['USA', 'USA', 'Canada', 'Canada', 'Mexico'],
        'region': [None, 'North', None, 'East', 'South'],
        'quantity': [10, None, 30, 40, None],
        'category': ['A', 'B', None, 'A', 'B'],
        'dealsize': ['small', 'medium', 'large', 's', 'm'],
        'date': ['2021-01-01 12:00:00', '01/02/2021', '03/01/2021', '2021/04/01', '2021-05-01'],
        'unit_price': [100, 200, 300, 400, 500],
        'total_price': [1000, 2000, 3000, 4000, 5000]
    }
    df = pd.DataFrame(data)

    df = impute_region(df)
    print("After impute_region:")
    print(df)

    df = impute_quantity(df)
    print("\nAfter impute_quantity:")
    print(df)

    df = impute_category(df)
    print("\nAfter impute_category:")
    print(df)

    df = handle_inconsistent_dealsize(df)
    print("\nAfter handle_inconsistent_dealsize:")
    print(df)

    df = handle_inconsistent_dates(df)
    print("\nAfter handle_inconsistent_dates:")
    print(df)

    outliers = retrieve_quantity_outliers(df)
    print("\nQuantity outliers:")
    print(outliers)

    df = handle_unit_price_outliers(df)
    print("\nAfter handle_unit_price_outliers:")
    print(df)

    df = normalize_total_price(df)
    print("\nAfter normalize_total_price:")
    print(df)

    df = normalize_quantity(df)
    print("\nAfter normalize_quantity:")
    print(df)

    df = normalize_unit_price(df)
    print("\nAfter normalize_unit_price:")
    print(df)