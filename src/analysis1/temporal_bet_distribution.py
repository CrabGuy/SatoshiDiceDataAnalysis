import pandas
from src.data_loading.data_loader import read_parquet
from src.plotting.plots import plot_time_distribution
from src.plotting.plot_map_popular import plot_map_popular

transactions = read_parquet("transactions")
satoshi_bets = transactions[transactions["is_satoshi_bet"]]
satoshi_bets.drop_duplicates(subset="transaction_id")

def temporal_distribution(bets: pandas.DataFrame, time_step = "1ME"):
    return bets.resample(time_step, on="timestamp").size()

plot_map_popular(
    amount_popular_dices=3,
    bets_dataframe=satoshi_bets,
    map_function=temporal_distribution,
    plot_function=plot_time_distribution
)