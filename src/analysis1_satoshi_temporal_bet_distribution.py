import pandas
from data_loader import read_parquet
from plots import plot_time_distribution
from plot_map import plot_map

transactions = read_parquet("transactions")
satoshi_bets = transactions[transactions["is_satoshi_bet"]]
satoshi_bets.drop_duplicates(subset="transaction_id")

def temporal_distribution(bets: pandas.DataFrame, time_step = "1W"):
    return bets.resample(time_step, on="timestamp").size()

plot_map(
    amount_popular_dices=3,
    bets_dataframe=satoshi_bets,
    map_function=temporal_distribution,
    plot_function=plot_time_distribution
)