import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import matplotlib.pyplot as plt


def style_plot(ax):
    """Style the plot.

    Args:
        ax (matplotlib.axes.Axes): Axes object.
    """
    plt.gca().yaxis.set_major_formatter(mticker.StrMethodFormatter("£{x:,.0f}"))
    ax.set(xlabel="", ylabel="", xlim=(1980, 2020))
    sns.despine(left=True, top=True, right=True, bottom=False)
    ax.yaxis.tick_right()
    # add grid lines to the plot for the y axis
    ax.yaxis.grid(True, color="slategray", alpha=0.1)
    # add annotation to most-expensive player
    ax.annotate(
        "Neymar",
        xy=(2016.7, 196000000),
        xytext=(2010, 170000000),
        arrowprops=dict(
            arrowstyle="-|>", color="black", connectionstyle="arc3,rad=0.3"
        ),
        color="black",
        fontsize=10,
    )
    ax.annotate(
        "Pogba",
        xy=(2016, 87000000),
        xytext=(2017, 60000000),
        arrowprops=dict(
            arrowstyle="-|>", color="black", connectionstyle="arc3,rad=-0.3"
        ),
        color="black",
        fontsize=10,
    )
    ax.annotate(
        "C. Ronaldo",
        xy=(2008.8, 80000000),
        xytext=(2002, 70000000),
        arrowprops=dict(
            arrowstyle="-|>", color="black", connectionstyle="arc3,rad=-0.3"
        ),
        color="black",
        fontsize=10,
    )
    ax.set_yticks([5000000, 50000000, 100000000, 150000000, 200000000], minor=False)
    ax.set_xticks([1980, 1990, 2000, 2010, 2020], minor=False)
    ax.set_xticklabels([], minor=False)
    ax.tick_params(axis="y", which="both", length=0)
    ax.tick_params(axis="x", which="both", length=5)
    ax.set_facecolor("#E1DFD0")


def annotate_plot(ax):
    """Annotate the graph.

    Args:
        ax (matplotlib.axes.Axes): Axes object.
    """
    ax.text(
        0.103,
        -0.05,
        "1980",
        fontsize=10,
        ha="left",
        transform=ax.transAxes,
    )
    ax.text(
        0.355,
        -0.05,
        "1990",
        fontsize=10,
        ha="left",
        transform=ax.transAxes,
    )
    ax.text(
        0.605,
        -0.05,
        "2000",
        fontsize=10,
        ha="left",
        transform=ax.transAxes,
    )
    ax.text(
        0.855,
        -0.05,
        "2010",
        fontsize=10,
        ha="left",
        transform=ax.transAxes,
    )
    ax.text(
        x=1980,
        y=200000000,
        s="MOST EXPENSIVE",
        color="black",
        fontsize=34,
        ha="left",
        va="center",
        fontweight=800,
    )
    ax.text(
        x=1980,
        y=180000000,
        s="FOOTBALL TRANSFERS",
        color="red",
        fontsize=26,
        ha="left",
        va="center",
        fontweight=800,
    )
    ax.text(
        x=1980,
        y=141000000,
        s=(
            "Discover the trend of transfers in football history, including\n"
            "Neymar's move to PSG, Ronaldo's transfer to Real Madrid, and\n"
            "Pogba's deal with Manchester United. This graph showcases the\n"
            "biggest splurges made by football clubs to secure top talent, providing\n"
            "a fascinating glimpse into the world of high-stakes transfers."
        ),
        color="black",
        fontsize=10,
        ha="left",
        va="center",
    )


def main():
    """Main function."""
    # Data scraped from Wikipedia
    # https://en.wikipedia.org/wiki/List_of_most_expensive_association_football_transfers

    df = pd.read_csv("transfer_records.csv")
    df = df[df["year"] >= 1980]
    fig, ax = plt.subplots(figsize=(10, 6))
    fig.set_facecolor("#E1DFD0")
    sns.scatterplot(
        data=df,
        x="year",
        y="value_gbp",
        size="value_gbp",
        sizes=(10, 300),
        legend=False,
        linewidth=0,
        color="#E3120B",
    )
    z = np.polyfit(df["year"], df["value_gbp"], 3)
    p = np.poly1d(z)
    sns.lineplot(
        data=df,
        x="year",
        y=p(df["year"]),
        linestyle="--",
        alpha=1,
        color="black",
    )
    style_plot(ax)
    annotate_plot(ax)
    plt.savefig("./images/slopes.png", dpi=300, bbox_inches="tight")


if __name__ == "__main__":
    main()
