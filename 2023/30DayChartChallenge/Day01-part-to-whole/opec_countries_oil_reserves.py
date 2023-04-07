import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Data scraped from https://asb.opec.org/ASB_Charts.html?chapter=223
DATA = [
    {"country": "Other", "reserves_bbl": 12.2 + 2.52 + 2 + 1.81 + 1.1},
    {"country": "Nigeria", "reserves_bbl": 37.05},
    {"country": "Libya", "reserves_bbl": 48.36},
    {"country": "Kuwait", "reserves_bbl": 101.5},
    {"country": "United Arab Emirates", "reserves_bbl": 111},
    {"country": "Iraq", "reserves_bbl": 145.02},
    {"country": "IR Iran", "reserves_bbl": 208.6},
    {"country": "Saudi Arabia", "reserves_bbl": 267.19},
    {"country": "Venezuela", "reserves_bbl": 303.47},
]

COLORS = ["#222", "#333", "#444", "#555", "#666", "#777", "#888", "#999", "#aaa"]


def main():
    """Main function."""
    df = pd.DataFrame(DATA)
    df.sort_values(by="reserves_bbl", ascending=False, inplace=True)
    plot_oil_reserves_between_opec_countries(df)


def func(pct: float, allvals: pd.Series) -> str:
    """Function to calculate the percentage of each country in the pie chart.
    Args:
        pct (float): Percentage of each country.
        allvals (pd.Series): Series with oil reserves data.
    Returns:
        str: String with percentage and absolute value of each country.
    """
    absolute = int(np.round(pct / 100.0 * np.sum(allvals)))
    return f"{pct:.1f}%\n({absolute:d} BBLS)"


def plot_oil_reserves_between_opec_countries(df: pd.DataFrame) -> None:
    """Plot oil reserves between OPEC countries.
    Args:
        df (pd.DataFrame): Dataframe with oil reserves data.
    """
    # Create a pieplot
    fig, ax = plt.subplots(
        figsize=(15, 15), subplot_kw=dict(aspect="equal"), facecolor="#f4f0e8"
    )
    wedges, texts, autotexts = plt.pie(
        df["reserves_bbl"],
        autopct=lambda pct: func(pct, df["reserves_bbl"]),
        pctdistance=0.85,
        textprops=dict(size=10, color="w", weight="bold", font="Menlo"),
        colors=COLORS,
    )

    # add props to pie chart showing the percentage of each country
    bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
    kw = dict(arrowprops=dict(arrowstyle="-"), bbox=bbox_props, zorder=0, va="center")

    for i, p in enumerate(wedges):
        ang = (p.theta2 - p.theta1) / 2.0 + p.theta1
        y = np.sin(np.deg2rad(ang))
        x = np.cos(np.deg2rad(ang))
        horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
        connectionstyle = f"angle,angleA=0,angleB={ang}"
        kw["arrowprops"].update({"connectionstyle": connectionstyle})
        ax.annotate(
            df["country"].to_list()[i],
            xy=(x, y),
            xytext=(1.35 * np.sign(x), 1.4 * y),
            horizontalalignment=horizontalalignment,
            font="Menlo",
            size=14,
            **kw,
        )

    # add a circle at the center to transform it in a donut chart
    my_circle = plt.Circle((0, 0), 0.7, color="#f4f0e8")
    p = plt.gcf()
    p.gca().add_artist(my_circle)

    # add oil pump image
    img = plt.imread("./oil-pump.png")
    newax = fig.add_axes([0.375, 0.375, 0.3, 0.3], zorder=1)
    newax.imshow(img)
    newax.axis("off")

    plt.savefig("oil_reserves.png", dpi=300, bbox_inches="tight", facecolor="#f4f0e8")


if __name__ == "__main__":
    main()
