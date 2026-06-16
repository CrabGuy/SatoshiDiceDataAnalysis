from data_loader import read_parquet
from plots import plot_bet_correlation
import pandas

satoshi_bets = read_parquet("satoshi_bets")

def bet_correlation(dataframe: pandas.DataFrame):
    print(f"Correlation: {dataframe["fee"].corr(dataframe["amount"])}")
    plot_bet_correlation(dataframe, "fee", "amount")

# TODO: Do this also for the other 2 most popular
bet_correlation(satoshi_bets[satoshi_bets["Name"] == "lessthan 32000"])