import matplotlib.pyplot as pyplot
pyplot.style.use('rose-pine-dawn')

def save_plot_image(name):
	pyplot.tight_layout()
	pyplot.savefig(f"../outputs/figures/{name}.png", dpi=300)
	pyplot.clf()

def plot_relative_transaction_percentage(dataframe):
	dataframe.plot(kind="line", figsize=(12, 6))
	save_plot_image("relative_transaction_percentage")


def plot_absolute_transaction_percentage(dataframe):
	dataframe.plot(kind="line", figsize=(12, 6))
	save_plot_image("absolute_transaction_percentage")

def plot_satoshi_dice_popularity(dataframe):
    top_amount = dataframe.sort_values("amount")

    fig, (ax1, ax2) = pyplot.subplots(1, 2, figsize=(16, 6))

    ax1.barh(top_amount["name"], top_amount["amount"] / 1e9)
    ax1.set_xscale("log")
    ax1.set_xlabel("Amount Spent")
    ax1.set_title("Top Addresses by Amount Spent")
    ax1.xaxis.set_major_formatter(pyplot.FuncFormatter(lambda x, _: f"{x:.1f}B"))

    ax2.barh(top_amount["name"], top_amount["count"] / 1e3)
    ax2.set_xscale("log")
    ax2.set_xlabel("Transaction Count (thousands)")
    ax2.set_title("Top Addresses by Transaction Count")
    ax2.xaxis.set_major_formatter(pyplot.FuncFormatter(lambda x, _: f"{x:.0f}K"))


    save_plot_image("satoshi_dice_popularity")

def plot_payout_distance_distribution(dataframe):
    fig, (ax1, ax2) = pyplot.subplots(1, 2, figsize=(16, 6))

    ax1.hist(dataframe, bins=50, edgecolor="black")
    ax1.set_xlabel("Block Distance")
    ax1.set_ylabel("Count")
    ax1.set_title("Bet to Payout Distance Distribution")

    ax2.hist(dataframe, bins=50, edgecolor="black")
    ax2.set_yscale("log")
    ax2.set_xlabel("Block Distance")
    ax2.set_ylabel("Count (log scale)")
    ax2.set_title("Bet to Payout Distance Distribution (log scale)")

    save_plot_image("payout_distance_distribution")

def plot_time_distribution(series, freq: str) -> None:
    ax = series.plot(kind='bar', figsize=(12, 4))
    ax.set_title(f'Transactions per {freq}')
    ax.set_xlabel('Time')
    ax.set_ylabel('Count')

    ax.set_xticklabels([ts.strftime('%Y-%m-%d') for ts in series.index])

    pyplot.xticks(rotation=45, ha='right')

    save_plot_image("popular_time_distribution")

def plot_bet_correlation(df, col1, col2):
    corr = df[col1].corr(df[col2])
    fig, ax = pyplot.subplots()
    ax.scatter(df[col1], df[col2], alpha=0.5, s=10)
    ax.set(xlabel=col1, ylabel=col2, title=f"{col1} vs {col2}  |  r = {corr:.2f}")
    ax.set_xlim(0, 0.04 * 1e8)
    ax.set_ylim(0, 2.5 * 1e8)

    save_plot_image("bet_correlation")

# TODO: Show better the distribution without the outlier and remove the time difference graph, only keep the distribution
def plot_bet_distance(series):
    fig, (ax1, ax2) = pyplot.subplots(1, 2, figsize=(16, 4))
    ax1.plot(series.values)
    ax1.set_xlabel("Index")
    ax1.set_ylabel("Time difference (s)")
    ax1.set_title("Time difference between consecutive timestamps")
    ax2.hist(series.dropna(), bins=50, edgecolor="black")
    ax2.set_yscale("log")
    ax2.set_xlabel("Time difference (s)")
    ax2.set_ylabel("Count (log scale)")
    ax2.set_title("Distribution (log scale)")

    save_plot_image("bet_distance")