from src.plotting.plots import plot_payout_distance_distribution
from src.data_loading.data_loader import read_parquet
import pandas

transactions = read_parquet("transactions", columns=["transaction_id", "transaction_block_id", "input_transaction_id", "timestamp", "is_satoshi_bet"])
# dropping transactions which don't have an input (which have not been spent yet)
transactions = transactions.dropna()

satoshi_payouts = pandas.merge(
    transactions,
    transactions[transactions["is_satoshi_bet"]],
    left_on="transaction_id",
    right_on="input_transaction_id"
)

block_delta = satoshi_payouts["transaction_block_id_y"] - satoshi_payouts["transaction_block_id_x"]
time_delta = satoshi_payouts["timestamp_y"] - satoshi_payouts["timestamp_x"]

print("Block:")
print(block_delta.describe())
print("Time:")
print(time_delta.describe())

plot_payout_distance_distribution(block_delta, time_delta)