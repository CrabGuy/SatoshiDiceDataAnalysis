import pandas

pandas.set_option('display.max_columns', None)
pandas.set_option('display.width', None)
pandas.set_option('display.max_colwidth', None)

def read_dataset(name, columns):
    return pandas.read_csv(f"./data/raw/{name}", header=None, engine='pyarrow', names=columns)

def save_parquet(dataframe: pandas.DataFrame, name):
    return dataframe.to_parquet(f"./data/processed/{name}.parquet", index=False)

def read_parquet(name, columns=None):
    return pandas.read_parquet(f"./data/processed/{name}.parquet", columns=columns)