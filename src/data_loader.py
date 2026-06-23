import pandas
pandas.set_option('display.max_columns', None)
pandas.set_option('display.width', None)
pandas.set_option('display.max_colwidth', None)

def read_dataset(name, columns):
    return pandas.read_csv(f"../data/raw/{name}", header=None, engine='pyarrow', names=columns)

def save_parquet(dataframe: pandas.DataFrame, name):
    return dataframe.to_parquet(f"../data/processed/{name}.parquet", index=False)

def read_parquet(name, columns=None):
    return pandas.read_parquet(f"../data/processed/{name}.parquet", columns=columns)

if __name__ == "__main__":
    # TODO: Input transaction id is a float?
    inputs = read_dataset("inputs.csv", ["transaction_id", "input_transaction_id", "input_transaction_position"])

    outputs = read_dataset("outputs.csv", ["transaction_id", "output_position", "output_address_id", "amount", "script_type"])
    outputs = outputs.drop(columns=["script_type"])
    invalid_outputs = outputs.duplicated(subset=["transaction_id", "output_position"], keep=False)
    print(f"Warning: there are {invalid_outputs.sum()} invalid outputs!")
    outputs = outputs[~invalid_outputs]

    transactions = read_dataset("transactions.csv", ["timestamp", "transaction_block_id", "transaction_id", "is_codebase", "transaction_fee"])
    transactions = transactions.drop(columns=["is_codebase"])
    invalid_transactions = transactions.duplicated(subset=["transaction_id"], keep=False)
    print(f"Warning: there are {invalid_transactions.sum()} invalid transactions!")
    # Not my data, not my problem
    transactions = transactions[~invalid_transactions]
    transactions["timestamp"] = pandas.to_datetime(transactions["timestamp"], unit="s")

    complete_transactions = transactions.merge(inputs, how="left").merge(outputs, how="left")

    mappings = read_dataset("mappings.csv", ["address_hash", "address_id"])

    satoshi_dices = pandas.read_csv("../satoshiDiceInfos.tsv", sep='\t')[["Name", "Address"]]
    satoshi_dices.columns = ["name", "address_hash"]
    satoshi_dices = satoshi_dices.merge(mappings)

    complete_transactions["is_satoshi_bet"] = complete_transactions["output_address_id"].isin(satoshi_dices["address_id"])

    # key = ["transaction_id", "input_transaction_id", "input_transaction_position", "output_position"]
    save_parquet(complete_transactions, "transactions")
    save_parquet(satoshi_dices, "satoshi_dices")
    # TODO: Include sanity checks everywhere