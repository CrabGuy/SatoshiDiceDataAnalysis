from data_loader import read_parquet

inputs = read_parquet("inputs")
outputs = read_parquet("outputs")
transactions = read_parquet("transactions")
satoshi_dices = read_parquet("satoshi_dices")
mappings = read_parquet("mappings")

satoshi_dices = set(satoshi_dices.merge(mappings, left_on="Address", right_on="hash")["address_id"])

transactions = inputs[["previous_transaction_id", "transaction_id"]].merge(transactions[["transaction_id"]]).merge(outputs[["transaction_id", "address_id"]])
transactions = transactions.rename(columns={"previous_transaction_id": "input_id", "address_id": "output_id"})


transactions["is_dice_output"] = transactions["output_id"].isin(satoshi_dices)

grouped = transactions.groupby('transaction_id')

mask = (
    grouped['input_id'].transform('nunique') == 1
) & (
    grouped['output_id'].transform('nunique') == 2
) & (
    grouped['is_dice_output'].transform("any")
)

simple_bets_transactions = transactions[mask]

simple_bets = (
    simple_bets_transactions
    .sort_values("is_dice_output")
    .groupby("transaction_id").agg(
        input_id = ("input_id", "first"),
        change_id = ("output_id", "first"),
        dice_id = ("output_id", "last")
    )
    .reset_index()
)

print(simple_bets)