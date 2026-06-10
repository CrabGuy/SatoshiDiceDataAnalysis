import pandas
import matplotlib.pyplot as pyplot
pyplot.style.use('rose-pine-dawn')


def read_dataset(name, columns):
    return pandas.read_csv(f"../dataset/{name}", header=None, engine='pyarrow', names=columns)

def save_plot_image(name):
	pyplot.tight_layout()
	# pyplot.yscale('log')
	pyplot.savefig(f"../plots/{name}.png", dpi=300)
	pyplot.clf()

inputs = read_dataset("inputs.csv", ["transaction_id", "previous_transaction_id", "previous_transaction_position"])

outputs = read_dataset("outputs.csv", ["transaction_id", "position", "address_id", "amount", "script_type"])

transactions = read_dataset("transactions.csv", ["timestamp", "block_id", "transaction_id", "is_codebase", "fee"])
transactions["timestamp"] = pandas.to_datetime(transactions["timestamp"], unit="s")

mappings = read_dataset("mappings.csv", ["hash", "address_id"])

satoshi_dices = pandas.read_csv("../satoshiDiceInfos.tsv", sep='\\s+')[["Name", "Address"]]

# TODO: Put the relative payouts operations in another file and optimize by filtering beforehand

# Satoshi payouts relative amounts

payouts = outputs.merge(mappings).merge(transactions)[["hash", "amount", "timestamp"]]
satoshi_payouts = payouts.merge(satoshi_dices, right_on="Address", left_on="hash")

def resample(dataframe, start):
	TIME_STEP = "1ME"
	return dataframe[dataframe["timestamp"].between(start, "2023-12-31")].resample(TIME_STEP, on="timestamp")

sampled_payouts = resample(payouts, satoshi_payouts["timestamp"].min()).size()
sampled_satoshi_payouts = resample(satoshi_payouts, satoshi_payouts["timestamp"].min()).size()

relative_amounts = (sampled_satoshi_payouts / sampled_payouts).rename("relative_amounts")
relative_amounts.plot(kind="line", figsize=(12, 5))

save_plot_image("relative_amounts")

pandas.DataFrame({
    "total": sampled_payouts,
    "satoshi": sampled_satoshi_payouts
}).plot(kind="line", figsize=(12, 5))

save_plot_image("comparative_amounts")