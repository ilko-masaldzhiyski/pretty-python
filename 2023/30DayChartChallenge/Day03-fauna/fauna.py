import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# https://www.fao.org/forest-resources-assessment/2020/en/
DATA = [
    {"period": "1990-2000", "deforestation": -16, "expansion": 8},
    {"period": "2000-2010", "deforestation": -15, "expansion": 10},
    {"period": "2010-2015", "deforestation": -12, "expansion": 7},
    {"period": "2015-2020", "deforestation": -10, "expansion": 5},
]


def main():
    """Main function."""
    df = pd.DataFrame(DATA)
    df_melt = df.melt(id_vars="period")
    style_plot(df_melt)


def style_plot(df_melt: pd.DataFrame) -> None:
    """Style the plot.

    Args:
        df_melt (pd.DataFrame): Melted dataframe.
    """
    fig, ax = plt.subplots(figsize=(10, 3))
    sns.barplot(
        data=df_melt,
        x="value",
        y="period",
        hue="variable",
        dodge=False,
        palette=["#E3120B", "#1F2E7A"],
    )
    sns.despine(left=True, bottom=True)
    ax.xaxis.tick_top()
    ax.grid(axis="x", color="#B3B3B3", linestyle="-", linewidth=1)
    ax.set_xlim(-20, 15)
    ax.tick_params(axis="both", which="both", length=0)
    ax.set_axisbelow(True)
    ax.legend().remove()
    ax.set_yticklabels(ax.get_yticklabels(), color="#333333")
    ax.text(
        x=0, y=2, s=" Expansion", color="white", fontsize=12, ha="left", va="center"
    )
    ax.text(
        x=0,
        y=0,
        s="Deforestation ",
        color="white",
        fontsize=12,
        ha="right",
        va="center",
    )
    ax.set(xlabel="", ylabel="")
    ax.axvline(x=0, ymin=0, ymax=1, color="#333333", linewidth=2)
    fig.set_facecolor("#E1DFD0")
    ax.set_facecolor("#E1DFD0")
    plt.savefig("./images/fauna.png", dpi=300, bbox_inches="tight", transparent=True)


if __name__ == "__main__":
    main()
