import pandas
from src.data_loading.data_loader import read_parquet
from src.plotting.plots import plot_bet_distance
from src.plotting.plot_map_popular import plot_map_popular

transactions = read_parquet("transactions")
satoshi_bets = transactions[transactions["is_satoshi_bet"]]
satoshi_bets = satoshi_bets.drop_duplicates(subset="transaction_id")

def bet_distance(dataframe: pandas.DataFrame):
    return dataframe.sort_values("transaction_block_id")["timestamp"].diff().dt.total_seconds()

plot_map_popular(
    amount_popular_dices=3,
    bets_dataframe=satoshi_bets,
    map_function=bet_distance,
    plot_function=plot_bet_distance
)