import numpy as np
import pandas as pd
import matplotlib.pyplot as pyplot

pyplot.style.use('rose-pine-dawn')


def save_plot_image(name):
    pyplot.tight_layout()
    pyplot.savefig(f"../outputs/figures/{name}.png", dpi=300)
    pyplot.clf()


def plot_relative_transaction_percentage(dataframe):
    dataframe = dataframe.drop(columns="transaction_id", errors="ignore")
    ax = dataframe.plot(kind="line", figsize=(12, 5), linewidth=1.5, marker="o", markersize=4)
    ax.set_title("Relative Transaction Percentage Over Time")
    ax.set_xlabel("Time")
    ax.set_ylabel("Percentage (%)")
    ax.legend(frameon=False)
    ax.spines[["top", "right"]].set_visible(False)
    save_plot_image("relative_transaction_percentage")


def plot_absolute_transaction_percentage(dataframe):
    dataframe = dataframe.drop(columns="transaction_id", errors="ignore")
    ax = dataframe.plot(kind="line", figsize=(12, 5), linewidth=1.5, marker="o", markersize=4)
    ax.set_title("Absolute Transaction Count Over Time")
    ax.set_xlabel("Time")
    ax.set_ylabel("Count")
    ax.legend(frameon=False)
    ax.spines[["top", "right"]].set_visible(False)
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


def plot_payout_distance_distribution(block_delta_dataframe, time_delta_dataframe):
    fig, (ax1, ax2) = pyplot.subplots(1, 2, figsize=(16, 6))

    ax1.hist(block_delta_dataframe, bins=50, edgecolor="black")
    ax1.set_xlabel("Block Distance")
    ax1.set_ylabel("Count")
    ax1.set_yscale("log")
    ax1.set_title("Bet to Payout Distance (Blocks)")

    time_delta = time_delta_dataframe.dropna()
    if not pd.api.types.is_timedelta64_dtype(time_delta):
        time_delta = pd.to_timedelta(time_delta, unit="s")
    data_unit = time_delta.values.dtype.name.split("[")[-1].rstrip("]")
    bin_edges = pd.to_timedelta(
        [0, 60, 300, 600, 1800, 3600, 21600, 86400, 3650 * 86400], unit="s"
    ).as_unit(data_unit)
    bin_labels = ["<1m", "1-5m", "5-10m", "10-30m", "30-60m", "1-6h", "6-24h", ">1d"]
    binned_counts = pd.cut(time_delta, bins=bin_edges, labels=bin_labels).value_counts().reindex(bin_labels)

    ax2.bar(bin_labels, binned_counts.values, edgecolor="black")
    ax2.set_xlabel("Time Distance")
    ax2.set_ylabel("Count")
    ax2.set_title("Bet to Payout Distance (Time)")
    ax2.tick_params(axis="x", rotation=45)

    save_plot_image("payout_distance_distribution")


def plot_time_distribution(series, index: int, freq: str = "Week") -> None:
    ax = series.plot(kind='bar', figsize=(12, 4))
    ax.set_title(f'Transactions per {freq}')
    ax.set_xlabel('Time')
    ax.set_ylabel('Count')
    ax.set_xticklabels([ts.strftime('%Y-%m-%d') for ts in series.index])
    pyplot.xticks(rotation=45, ha='right')
    save_plot_image(f"popular_time_distribution_{index + 1}")


def plot_bet_correlation(df, index, col1="transaction_fee", col2="amount"):
    corr = df[col1].corr(df[col2])
    fig, ax = pyplot.subplots()
    ax.scatter(df[col1], df[col2], alpha=0.5, s=10)
    ax.set(xlabel=col1, ylabel=col2, title=f"{col1} vs {col2}  |  r = {corr:.2f}")
    ax.set_xlim(0, 0.04 * 1e8)
    ax.set_ylim(0, 2.5 * 1e8)
    save_plot_image(f"bet_correlation_{index + 1}")


def plot_bet_distance(series, index):
    data = series.dropna()
    data = data[data > 0]
    bins = np.logspace(np.log10(data.min()), np.log10(data.max()), 50)

    fig, ax = pyplot.subplots(figsize=(8, 5))
    ax.hist(data, bins=bins, edgecolor="black")
    ax.set_xscale("log")
    ax.set_xlabel("Time difference (s)")
    ax.set_ylabel("Count")
    ax.set_title("Distribution of Time Between Consecutive Bets")
    save_plot_image(f"bet_distance_{index + 1}")


def plot_chain_length_distribution(length_distribution):
    fig, ax = pyplot.subplots(figsize=(8, 5))
    ax.bar(length_distribution.index, length_distribution.values)
    ax.set_yscale("log")
    ax.set_xlabel("Chain Length")
    ax.set_ylabel("Count")
    ax.set_title("Chain Length Distribution (log scale)")
    save_plot_image("chains_length_distribution")