import pandas
from data_loader import read_parquet
from plots import plot_bet_distance

satoshi_bets = read_parquet("satoshi_bets")


def bet_distance(dataframe: pandas.DataFrame):
    plot_bet_distance(dataframe.sort_values("block_id")["timestamp"].diff().dt.total_seconds())

# TODO: Do this also for the other 2 most popular
bet_distance(satoshi_bets[satoshi_bets["Name"] == "lessthan 32000"])