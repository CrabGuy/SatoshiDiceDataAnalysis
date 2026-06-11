import pandas

def read_dataset(name, columns):
    return pandas.read_csv(f"../data/raw/{name}", header=None, engine='pyarrow', names=columns)

def save_parquet(dataframe: pandas.DataFrame, name):
    return dataframe.to_parquet(f"../data/processed/{name}.parquet", index=False)

inputs = read_dataset("inputs.csv", ["transaction_id", "previous_transaction_id", "previous_transaction_position"])
save_parquet(inputs, "inputs")

outputs = read_dataset("outputs.csv", ["transaction_id", "position", "address_id", "amount", "script_type"])
outputs = outputs.drop(columns=["script_type"])
save_parquet(outputs, "outputs")

transactions = read_dataset("transactions.csv", ["timestamp", "block_id", "transaction_id", "is_codebase", "fee"])
transactions = transactions.drop(columns=["is_codebase", "fee"])
transactions["timestamp"] = pandas.to_datetime(transactions["timestamp"], unit="s")
save_parquet(transactions, "transactions")

mappings = read_dataset("mappings.csv", ["hash", "address_id"])
save_parquet(mappings, "mappings")

satoshi_dices = pandas.read_csv("../satoshiDiceInfos.tsv", sep='\t')[["Name", "Address"]]
save_parquet(satoshi_dices, "satoshi_dices")

transactions_amount = outputs.merge(mappings).merge(transactions)[["hash", "amount", "timestamp", "transaction_id", "position"]]
save_parquet(transactions_amount, "transactions_amount")

satoshi_bets = transactions_amount.merge(satoshi_dices, right_on="Address", left_on="hash")
satoshi_bets = satoshi_bets.drop(columns=["Address"])
save_parquet(satoshi_bets, "satoshi_bets")

# TODO: This is probably wrong, its not merging correctly
satoshi_payouts = inputs.merge(satoshi_bets, left_on="previous_transaction_id", right_on="transaction_id")
satoshi_payouts = satoshi_payouts.drop(columns=["previous_transaction_id"])

save_parquet(satoshi_payouts, "satoshi_payouts")