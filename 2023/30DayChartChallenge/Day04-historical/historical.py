import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

# Scraped from https://www.statista.com/statistics/564769/airline-industry-number-of-flights/
DATA = [
    {"year": 2012, "flights": 31.2},
    {"year": 2013, "flights": 32.0},
    {"year": 2014, "flights": 33.0},
    {"year": 2015, "flights": 34.0},
    {"year": 2016, "flights": 35.2},
    {"year": 2017, "flights": 36.4},
    {"year": 2018, "flights": 38.1},
    {"year": 2019, "flights": 38.9},
    {"year": 2020, "flights": 16.9},
    {"year": 2021, "flights": 20.1},
    {"year": 2022, "flights": 33.8},
]


def annotate_graph(ax):
    """Annotate the graph.

    Args:
        ax (matplotlib.axes.Axes): Axes object.
    """
    ax.text(
        x=2012,
        y=45,
        s="NUMBER OF FLIGHTS",
        color="white",
        fontsize=27,
        ha="left",
        va="center",
        fontweight=800,
    )
    ax.text(
        x=2012,
        y=43.5,
        s="HISTORIC DECLINE",
        color="red",
        fontsize=30.5,
        ha="left",
        va="center",
        fontweight=800,
    )
    ax.text(
        x=2012,
        y=41,
        s=(
            "The number of flights performed globally by the airline industry\n"
            "increased steadily since the early 2000s and reached 38.9M in\n"
            "2019. However, due to the coronavirus pandemic, the number\n"
            "of flights dropped to 16.9M in 2020."
        ),
        color="white",
        fontsize=10,
        ha="left",
        va="center",
    )
    # set x axis ticks to bold
    for tick in ax.get_xticklabels():
        tick.set_fontweight("bold")

    # add annotation to 2020 data point saying COVID-19. The arrow should be angled and colored in white
    ax.annotate(
        "COVID-19",
        xy=(2020, 16.9),
        xytext=(2019.92, 22),
        arrowprops=dict(
            arrowstyle="-|>", color="white", connectionstyle="arc3,rad=-0.1"
        ),
        color="white",
        fontsize=10,
        fontweight=800,
    )


def style_plot(fig, ax, df):
    """Style the plot.

    Args:
        fig (matplotlib.figure.Figure): Figure object.
        ax (matplotlib.axes.Axes): Axes object.
        df (pandas.DataFrame): DataFrame object.
    """
    ax.set(
        xlabel="",
        ylabel="",
        ylim=(15, 48),
        xticks=[int(x) for x in df["year"]],
        yticks=[20, 30, 40, 48],
    )
    sns.despine(left=True, top=True, right=False)
    ax.tick_params(axis="both", which="both", length=0)
    ax.yaxis.tick_right()
    ax.grid(axis="y", color="lightgrey", linewidth=0.5, alpha=0.1)
    ax.set_facecolor("black")
    fig.set_facecolor("black")
    ax.tick_params(colors="white")
    ax.xaxis.set_tick_params(pad=10)


def add_image(ax):
    """Add image to plot.

    Args:
        ax (matplotlib.axes.Axes): Axes object.
    """
    img = plt.imread("./images/coronavirus.png")
    imagebox = OffsetImage(img, zoom=0.08)
    ab = AnnotationBbox(imagebox, (2020.45, 24), frameon=False)
    ax.add_artist(ab)


def main():
    """Main function."""
    df = pd.DataFrame(DATA)
    fig, ax = plt.subplots(figsize=(10, 10))
    sns.lineplot(data=df, x="year", y="flights", color="tab:red", linewidth=2)
    plt.fill_between(df["year"], df["flights"], alpha=0.3, color="salmon")
    style_plot(fig, ax, df)
    annotate_graph(ax)
    add_image(ax)
    plt.savefig("./images/historical.png", dpi=300, bbox_inches="tight")


if __name__ == "__main__":
    main()
