import numpy as np
import pandas as pd
import matplotlib.pyplot as pyplot

pyplot.style.use('rose-pine-dawn')

def is_running_in_notebook() -> bool:
    try:
        from IPython import get_ipython
        shell = get_ipython().__class__.__name__
        return shell == "ZMQInteractiveShell"
    except (NameError, ImportError):
        return False

def save_plot_image(name):
    pyplot.tight_layout()
    pyplot.savefig(f"./outputs/figures/{name}.png", dpi=300)

    if is_running_in_notebook():
        pyplot.show()

    pyplot.clf()

def plot_relative_transaction_percentage(dataframe):
    dataframe = dataframe.drop(columns="transaction_id", errors="ignore")
    ax = dataframe.plot(kind="line", figsize=(12, 5), linewidth=1.5, marker="o", markersize=4)
    ax.set_title("Relative Transaction Percentage Over Time")
    ax.set_xlabel("Time")
    ax.set_ylabel("Percentage (%)")
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


def plot_payout_distance_distribution(block_delta_dataframe, time_delta_dataframe, num_outlier_bins=20):
    fig, (ax1, ax2, ax3) = pyplot.subplots(1, 3, figsize=(22, 6))

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
        [0, 60, 300, 600, 1800, 3600, 21600, 86400, 259200, 604800, 3650 * 86400],
        unit="s",
    ).as_unit(data_unit)
    bin_labels = ["<1m", "1-5m", "5-10m", "10-30m", "30-60m", "1-6h", "6-24h", "1-3d", "3-7d", ">7d"]
    binned_counts = pd.cut(time_delta, bins=bin_edges, labels=bin_labels).value_counts().reindex(bin_labels)
    ax2.bar(bin_labels, binned_counts.values, edgecolor="black")
    ax2.set_xlabel("Time Distance")
    ax2.set_ylabel("Count")
    ax2.set_title("Bet to Payout Distance (Time)")
    ax2.tick_params(axis="x", rotation=45)

    seven_days = pd.to_timedelta(7, unit="D")
    outliers_days = (time_delta[time_delta > seven_days].dt.total_seconds() / 86400).values

    if len(outliers_days) > 0:
        min_d, max_d = outliers_days.min(), outliers_days.max()
        if min_d == max_d:
            ax3.scatter([min_d], [len(outliers_days)], s=30, edgecolor="black", linewidth=0.5)
        else:
            bins = np.logspace(np.log10(min_d), np.log10(max_d), num=num_outlier_bins)
            counts, bin_edges_outliers = np.histogram(outliers_days, bins=bins)
            bin_centers = np.sqrt(bin_edges_outliers[:-1] * bin_edges_outliers[1:])
            mask = counts > 0
            ax3.scatter(bin_centers[mask], counts[mask], s=30, edgecolor="black", linewidth=0.5)
        ax3.set_xscale("log")
        ax3.set_yscale("log")
    else:
        ax3.text(0.5, 0.5, "No outliers >7d", ha="center", va="center", transform=ax3.transAxes)

    ax3.set_xlabel("Time Distance (days, >7d only)")
    ax3.set_ylabel("Count")
    ax3.set_title("Bet to Payout Distance Outliers (>7d, log-binned)")

    save_plot_image("payout_distance_distribution")


def plot_time_distribution(items: list, freq: str = "Month") -> None:
    fig, axes = pyplot.subplots(len(items), 1, figsize=(12, 4 * len(items)))
    if len(items) == 1:
        axes = [axes]

    for ax, (series, index) in zip(axes, items):
        series.plot(kind='bar', ax=ax)
        ax.set_title(f'Transactions per {freq} ({index})')
        ax.set_xlabel('Time')
        ax.set_ylabel('Count')
        ax.set_xticklabels([ts.strftime('%Y-%m-%d') for ts in series.index])
        ax.tick_params(axis='x', rotation=45)
        for label in ax.get_xticklabels():
            label.set_ha('right')

    pyplot.tight_layout()
    save_plot_image("popular_time_distribution")


def plot_bet_correlation(items: list, col1="transaction_fee", col2="amount"):
    fig, axes = pyplot.subplots(1, len(items), figsize=(6 * len(items), 6))
    if len(items) == 1:
        axes = [axes]

    for ax, (df, index) in zip(axes, items):
        corr = df[col1].corr(df[col2])
        ax.scatter(df[col1], df[col2], alpha=0.5, s=10)
        ax.set(xlabel=col1, ylabel=col2, title=f"{col1} vs {col2} ({index})  |  r = {corr:.2f}")
        ax.set_xlim(0, 0.04 * 1e8)
        ax.set_ylim(0, 2.5 * 1e8)

    pyplot.tight_layout()
    save_plot_image("bet_correlation")


def plot_bet_distance(items: list):
    fig, axes = pyplot.subplots(1, len(items), figsize=(8 * len(items), 5))
    if len(items) == 1:
        axes = [axes]

    for ax, (series, index) in zip(axes, items):
        data = series.dropna()
        data = data[data > 0]
        bins = np.logspace(np.log10(data.min()), np.log10(data.max()), 50)
        ax.hist(data, bins=bins, edgecolor="black")
        ax.set_xscale("log")
        ax.set_xlabel("Time difference (s)")
        ax.set_ylabel("Count")
        ax.set_title(f"Distribution of Time Between Consecutive Bets ({index})")

    pyplot.tight_layout()
    save_plot_image("bet_distance")


def plot_chain_length_distribution(paths_lengths):
    lengths = np.array(paths_lengths)
    lengths = lengths[lengths > 0]

    min_len, max_len = lengths.min(), lengths.max()
    bins = np.logspace(np.log10(min_len), np.log10(max_len), num=30)

    counts, bin_edges = np.histogram(lengths, bins=bins)
    bin_centers = np.sqrt(bin_edges[:-1] * bin_edges[1:])
    widths = np.diff(bin_edges)

    mask = counts > 0
    density = counts[mask] / widths[mask]  # normalize by bin width

    fig, ax = pyplot.subplots(figsize=(8, 5))
    ax.scatter(bin_centers[mask], density, s=30, color="#a8417a")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("Chain Length")
    ax.set_ylabel("Density (count / bin width)")
    ax.set_title("Chain Length Distribution (log-log, log-binned)")
    save_plot_image("chains_length_distribution")