from plots import plot_payout_distance_distribution
from data_loader import read_parquet

transactions = read_parquet("transactions", columns=["transaction_id", "transaction_block_id", "input_transaction_id", "timestamp", "is_satoshi_bet"])
# dropping transactions which don't have an input (which have not been spent yet)
transactions = transactions.dropna()

# TODO: IMPORTANT FIX THIS BBY ADDING INPUT POSITION
satoshi_payouts = transactions.merge(
    transactions[transactions["is_satoshi_bet"]],
    left_on="transaction_id",
    right_on="input_transaction_id"
)
satoshi_payouts = satoshi_payouts.drop_duplicates(subset=["transaction_id_x", "transaction_id_y"])

block_delta = satoshi_payouts["transaction_block_id_y"] - satoshi_payouts["transaction_block_id_x"]
time_delta = satoshi_payouts["timestamp_y"] - satoshi_payouts["timestamp_x"]

print("Time:")
print(time_delta.describe())
print("Block:")
print(block_delta.describe())

plot_payout_distance_distribution(block_delta)