import pandas as pd
import time
import pyarrow.parquet as pq

def create_multi_index_df(dataframe: pd.DataFrame) -> pd.DataFrame:
    sorted_df = dataframe.sort_values(['year', 'region'])
    multi_index_df = sorted_df.set_index(['year', 'region'])
    return multi_index_df

def retrieve_multi_index_data(dataframe: pd.DataFrame, year: int, region: str) -> pd.DataFrame:
    try:
        result = dataframe.loc[(year, region)]
        if isinstance(result, pd.Series):
            return result.to_frame().T
        return result
    except KeyError:
        print(f"No data found for year {year} and region {region}")
        return pd.DataFrame()

def multi_index_aggregate(dataframe: pd.DataFrame) -> pd.DataFrame:
    return dataframe.groupby(['year', 'region']).agg({
        'quantity': 'sum',
        'total_price': 'sum'
    }).round(2)

def columns_multi_index(dataframe: pd.DataFrame) -> pd.DataFrame:
    return dataframe.groupby(['year', 'region', 'category']).agg({
        'quantity': 'sum',
        'total_price': 'sum'
    }).unstack(level='category').round(2)

def swap_columns_multi_index(dataframe: pd.DataFrame) -> pd.DataFrame:
    if not isinstance(dataframe.columns, pd.MultiIndex):
        raise ValueError("Input DataFrame must have multi-index columns")
    dataframe = dataframe.swaplevel(axis=1)
    dataframe = dataframe.sort_index(axis=1)
    return dataframe

def retrieve_multi_index_column(dataframe: pd.DataFrame, category: str) -> pd.DataFrame:
    return dataframe.xs(category, axis=1, level=0)

def retrieve_multi_index_basic(dataframe: pd.DataFrame, category: str, year: int) -> pd.DataFrame:
    return dataframe.loc[year].xs(category, axis=1, level=0)

def retrieve_multi_index_advanced(dataframe: pd.DataFrame, region: str, sub_column: str) -> pd.DataFrame:
    return dataframe.loc[(slice(None), region), (slice(None), sub_column)]

def create_pivot_table_basic(dataframe: pd.DataFrame) -> pd.DataFrame:
    return pd.pivot_table(dataframe, values=['quantity', 'total_price'],
                          index=['year', 'region'],
                          columns='category',
                          aggfunc='sum').round(2)

def create_pivot_table_advanced(dataframe: pd.DataFrame) -> pd.DataFrame:
    pivot = pd.pivot_table(dataframe,
                           values=['quantity', 'total_price', 'price'],
                           index=['year', 'region'],
                           columns='category',
                           aggfunc={'quantity': ['sum', 'mean'],
                                    'total_price': ['sum', 'mean'],
                                    'price': 'mean'}).round(2)
    return pivot.swaplevel(axis=1).sort_index(axis=1)

def avg_price_rolling_window(dataframe: pd.DataFrame) -> pd.DataFrame:
    dataframe['date'] = pd.to_datetime(dataframe['date'])
    dataframe = dataframe.sort_values('date').set_index('date')
    dataframe['rolling_avg'] = dataframe['total_price'].rolling(window='7D', min_periods=3).mean().round(2)
    return dataframe

def highlight_outliers(dataframe: pd.DataFrame) -> pd.DataFrame:
    dataframe['outliers'] = dataframe['total_price'] > 2.5 * dataframe['rolling_avg']
    return dataframe

def add_year_region_columns(dataframe: pd.DataFrame) -> pd.DataFrame:
    dataframe['year'] = pd.to_datetime(dataframe['FL_DATE']).dt.year
    dataframe['region'] = 'some_region'
    return dataframe

if __name__ == "__main__":
    filename = "/Users/kyrie/PycharmProjects/jour6/flights.parquet"
    df = pd.read_parquet(filename)


    print("Columns in the DataFrame:")
    print(df.columns)


    if 'year' in df.columns and 'region' in df.columns:
        multi_index_df = create_multi_index_df(df)
        print("Multi-index DataFrame:")
        print(multi_index_df.head())

        year = 2006
        region = "some_region"
        retrieved_data = retrieve_multi_index_data(multi_index_df, year, region)
        print(f"\nData for year {year} and region {region}:")
        print(retrieved_data)

        aggregated_data = multi_index_aggregate(multi_index_df)
        print("\nAggregated data:")
        print(aggregated_data)

        pivot_table = create_pivot_table_basic(df)
        print("\nPivot table:")
        print(pivot_table)
    else:
        print("The DataFrame does not contain the required 'year' and 'region' columns.")