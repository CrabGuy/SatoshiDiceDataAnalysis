import pandas
from data_loader import read_parquet
from plots import plot_time_distribution

transactions = read_parquet("transactions")
satoshi_bets = transactions[transactions["is_satoshi_bet"]]

print(satoshi_bets.columns)

def temporal_distribution(bets: pandas.DataFrame):
    bets = bets.drop_duplicates(subset="transaction_id")
    plot_time_distribution(bets.resample("1W", on="timestamp").size(), "Week")

# TODO: Do this also for the other 2 most popular
MOST_POPULAR_DICE_ID = 3524394
temporal_distribution(satoshi_bets[satoshi_bets["output_address_id"] == MOST_POPULAR_DICE_ID])