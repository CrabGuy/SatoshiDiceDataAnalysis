import pandas
from plots import plot_payout_distance_distribution

satoshi_payouts = pandas.read_parquet("../data/processed/satoshi_payouts.parquet")

# TODO: this is most likely correct but need to correct the merging
payout_distance = satoshi_payouts["position"] - satoshi_payouts["previous_transaction_position"]

plot_payout_distance_distribution(payout_distance)