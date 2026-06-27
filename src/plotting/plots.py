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


def plot_payout_distance_distribution(block_delta_dataframe):
    fig, ax1 = pyplot.subplots(figsize=(12, 5))
    ax1.hist(block_delta_dataframe, bins=20, edgecolor="black")
    ax1.set_xlabel("Block Distance")
    ax1.set_ylabel("Count")
    ax1.set_yscale("log")
    ax1.set_title("Bet to Payout Distance (Blocks)")

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

    rng = np.random.default_rng(42)

    for ax, (df, index) in zip(axes, items):
        corr = df[col1].corr(df[col2])

        x = df[col1].to_numpy()
        y = df[col2].to_numpy()

        x_jitter_scale = 0.01 * (0.04 * 1e8)
        y_jitter_scale = 0.01 * (2.5 * 1e8)

        x_jit = x + rng.normal(0, x_jitter_scale, size=len(x))
        y_jit = y + rng.normal(0, y_jitter_scale, size=len(y))

        ax.scatter(x, y, alpha=0.35, s=8, color="C0", linewidths=0)
        ax.scatter(x_jit, y_jit, alpha=0.15, s=8, color="C0", linewidths=0)

        ax.set(xlabel=col1, ylabel=col2, title=f"{col1} vs {col2} ({index})  |  r = {corr:.2f}")
        ax.set_xlim(0, 0.04 * 1e8)
        ax.set_ylim(0, 2.5 * 1e8)

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