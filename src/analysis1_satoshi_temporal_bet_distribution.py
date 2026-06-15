import pandas
from data_loader import read_parquet
from plots import plot_time_distribution

satoshi_bets = read_parquet("satoshi_bets")

print(satoshi_bets.columns)

def temporal_distribution(bets: pandas.DataFrame):
    plot_time_distribution(bets.resample("1W", on="timestamp").size(), "Week")

# TODO: Do this also for the other 2 most popular
temporal_distribution(satoshi_bets[satoshi_bets["Name"] == "lessthan 32000"])