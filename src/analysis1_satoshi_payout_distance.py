from plots import plot_payout_distance_distribution
from data_loader import read_parquet

inputs = read_parquet("inputs")
transactions = read_parquet("transactions")
satoshi_bets = read_parquet("satoshi_bets")

# TODO: Could probably optimize this further
satoshi_inputs = inputs[inputs["previous_transaction_id"].isin(satoshi_bets["transaction_id"].unique())]
inputs_block = satoshi_inputs.merge(transactions)

transaction_connection = inputs_block.merge(satoshi_bets, left_on="previous_transaction_id", right_on="transaction_id")

plot_payout_distance_distribution(transaction_connection["block_id_x"] - transaction_connection["block_id_y"])