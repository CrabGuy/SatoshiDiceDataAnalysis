import pandas
from plots import plot_absolute_transaction_percentage, plot_relative_transaction_percentage

transactions_amount = pandas.read_parquet("../data/processed/transactions_amount.parquet")
satoshi_bets = pandas.read_parquet("../data/processed/satoshi_bets.parquet")

def resample(dataframe, start):
	TIME_STEP = "1ME"
	return dataframe[dataframe["timestamp"].between(start, "2023-12-31")].resample(TIME_STEP, on="timestamp")

sampled_transactions_amount = resample(transactions_amount, satoshi_bets["timestamp"].min()).size()
sampled_satoshi_bets = resample(satoshi_bets, satoshi_bets["timestamp"].min()).size()

relative_amounts = (sampled_satoshi_bets / sampled_transactions_amount * 100).rename("relative_amounts")
plot_relative_transaction_percentage(relative_amounts)

plot_absolute_transaction_percentage(pandas.DataFrame({
    "total": sampled_transactions_amount,
    "satoshi": sampled_satoshi_bets
}))