import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from IPython.display import HTML
from pandas.io.formats.style import Styler


CUSTOM_STYLE = [
    # Table column headers
    {
        "selector": "th:not(.index_name)",
        "props": [
            ("background-color", "white"),
            ("color", "black"),
            ("font-size", "16px"),
            ("font-weight", "bold"),
            ("font-family", "Archivo"),
            ("white-space", "nowrap"),
        ],
    },
    # Table caption (at the bottom)
    {
        "selector": "caption",
        "props": [
            ("font-size", "16px"),
            ("font-family", "Archivo"),
            ("color", "black"),
            ("margin-bottom", "4px"),
            ("white-space", "nowrap"),
            ("caption-side", "bottom"),
        ],
    },
    # Table rows
    {
        "selector": "tr",
        "props": [
            ("background-color", "white"),
            ("border", "1px solid #f2f2f2 !important"),
        ],
    },
    # Table data
    {
        "selector": "td",
        "props": [
            ("text-align", "left"),
            ("color", "black"),
            ("font-size", "18px"),
            ("border", "1px solid #f2f2f2"),
            ("white-space", "nowrap"),
        ],
    },
]


def plot_sparklines(df: pd.DataFrame, ticker: str) -> None:
    """Plot each individual sparkline and store it for later use

    Visualizing images in a DataFrame is possible if we store them and later on
    treat them as if it's an HTML image that should be shown in the cell

    We'll be plotting a lineplot with the area underneath colored as well
    We'll be adding a scatterplot on top of the lineplot to show the actual
    values for the first and last year

    Args:
        df: The data we'll be plotting
        ticker: The ticker of the company used in the file name when saving
    """
    fig, ax = plt.subplots(figsize=(5, 1))
    df.sort_values(by="Year", inplace=True)
    sns.lineplot(data=df, x="Year", y="Number", color="black")
    plt.fill_between(
        df["Year"].to_list(),
        df["Number"].to_list(),
        alpha=0.15,
        color="slategray",
        linewidth=0,
    )
    df_subset = df[df["Year"].isin([2009, 2019, 2022])]
    sns.scatterplot(
        data=df_subset,
        x="Year",
        y="Number",
        s=50,
        linewidth=0,
        color=["black", "blue", "black"],
        zorder=2,
        clip_on=False,
    )
    ax.set(xlabel="", ylabel="", xticklabels=[], xticks=[], yticklabels=[], yticks=[])
    sns.despine(left=True, bottom=True)
    plt.savefig(
        f"graphs/{ticker}.svg",
        bbox_inches="tight",
        transparent=True,
    )


def add_delta_column(count_first_year: int, count_last_year: int) -> str:
    """Add a column indicating the direction of the change and its value

    We'll be showing a green arrow pointing upwards if the direction is positive
    We'll be showing a red arrow pointing downwards if the direction is negative
    We'll be showing a gray dash if there is no change

    The returned value needs to be formatted as HTML in order to show both the
    colored SVG icon and the delta itself

    Args:
        count_first_year: The value of the metric for the first year
        count_last_year: The value of the metric for the last year

    Returns:
        An HTML formatted string including the image with the direction
        and the value of the change
    """
    if count_last_year == 0 and count_first_year == 0:
        return ""
    elif count_last_year - count_first_year > 0:
        delta = (abs(count_first_year - count_last_year) / count_first_year) * 100
        delta = int(delta) if delta % 1 == 0 else round(delta, 1)
        delta = (
            '<span><img src="images/arrow-up-solid.svg" width="10" '
            'style="display:inline; margin-left: 5px; margin-right:'
            f'5px; padding-bottom: 2px;"/>{delta}%</span>'
        )
        return delta
    elif count_first_year - count_last_year > 0:
        delta = (abs(count_first_year - count_last_year) / count_first_year) * 100
        delta = int(delta) if delta % 1 == 0 else round(delta, 1)
        delta = (
            '<span><img src="images/arrow-down-solid.svg" width="10" '
            'style="display:inline; margin-left: 5px; margin-right:'
            f'5px; padding-bottom: 2px;"/>{delta}%</span>'
        )
        return delta
    else:
        delta = (
            '<span><img src="images/minus-solid.svg" width="10" '
            'style="display:inline; margin-left: 5px; margin-right:'
            '5px; padding-bottom: 2px;"/>0%</span>'
        )
        return delta


def produce_summary(df: pd.DataFrame, ticker: str) -> pd.DataFrame:
    """Generate a dataframe with the images and graphs we want to show

    The resulting dataframe will contain images and HTML code that needs to
    be parsed through pandas styling

    Args:
        df: A group from the original dataframe filtered on the company ticker
        ticker: The name of the ticker that this df is filtered on

    Returns:
        The calculated and graphed results for the given ticker
    """
    count_first_year = df[df["Year"] == df["Year"].min()]["Number"].values[0]
    count_last_year = df[df["Year"] == df["Year"].max()]["Number"].values[0]
    company = df["Company"].values[0]
    rows_list = []
    current_row = {}
    current_row["COMPANY"] = (
        '<div style="display:flex; align-items: center; justify-content: left">'
        f'<div><img src="images/{ticker}.png" style="max-width: 40px"/></div>'
        '<div style="padding-left:20px;">'
        '<p style="text-align: left; margin-bottom:4px;">'
        f"<strong>{company}</strong></p>"
        '<p style="text-align: left; color: #A2A2A2; margin-top: 4px; '
        f'margin-bottom:18px; font-size: 12px !important">SYMBL: {ticker}</p>'
        "</div></div>"
    )
    current_row["# EMPLOYEES"] = f"{count_last_year:,}"
    current_row["TREND"] = (
        f'<img src="graphs/{ticker}.svg" width="150" '
        'style="padding:0; margin:0; max-height: 60px;"/>'
    )
    plot_sparklines(df, ticker)
    for year in (2021, 2019, 2012):
        df_subset = df[df["Year"] >= year].copy()
        count_first_year = df_subset[df_subset["Year"] == df_subset["Year"].min()][
            "Number"
        ].values[0]
        count_last_year = df_subset[df_subset["Year"] == df_subset["Year"].max()][
            "Number"
        ].values[0]
        delta = add_delta_column(count_first_year, count_last_year)
        current_row[f"{2022-year}Y"] = delta
    rows_list.append(current_row)
    return pd.DataFrame(rows_list)


def style_table(df: pd.DataFrame) -> pd.DataFrame:
    """Style the table

    We create a custom styler so that we can have a title at the top
    and a footer at the bottom. We're using the caption as a footer
    and the title as a header

    Args:
        df: The dataframe to be styled
    Returns:
        The styled dataframe
    """

    MyStyler = Styler.from_custom_template(
        searchpath="", html_table="html_template.tpl"
    )
    styler = MyStyler(df.sort_values(by="COMPANY"))
    df_result = (
        styler.format()
        .hide()
        .set_table_styles(CUSTOM_STYLE)
        .set_properties(
            subset=["1Y", "3Y", "10Y"],
            **{
                "border-left": "2.5px solid #f2f2f2 !important",
                "border-right": "1px solid white !important",
                "padding-left": "10px !important",
                "padding-right": "10px !important",
            },
        )
        .set_properties(
            subset=["COMPANY"],
            **{
                "border-left": "0px !important",
                "border-right": "0px !important",
            },
        )
        .set_properties(
            subset=["# EMPLOYEES"],
            **{
                "border-left": "0px !important",
                "border-right": "0px !important",
                "text-align": "center !important",
                "font-weight": "bold",
            },
        )
        .set_properties(
            subset=["TREND"],
            **{"border-left": "0px !important", "text-align": "center !important"},
        )
        .set_caption(  # This would probably be better if added to the template
            (
                '<div style="display: flex; justify-content:space-between">'
                '<div style="order: 1">'
                '<span style="text-align:left; display: inline; color: #787878;'
                'font-size: 12px;"> Source: <strong>macrotrends.net</strong> | '
                "Number of employees in tech</span> </div>"
                '<div style="order:2">'
                '<img style="margin-bottom:-2px; display:inline" '
                'src="images/twitter.svg" width=12/>'
                '<span style="color: #787878; font-size:12px; text-align:right">'
                " @masaldzhiyski&nbsp;&nbsp;&nbsp;</span>"
                '<img style="margin-bottom:-2px; display:inline" '
                'src="images/github.svg" width=12/>'
                '<span style="color: #787878; font-size:12px; text-align:right">'
                " ilko-masaldzhiyski&nbsp;&nbsp;&nbsp;</span>"
                '<img style="margin-bottom:-2px; display:inline" '
                'src="images/linkedin.svg" width=12/>'
                '<span style="color: #787878; font-size:12px; text-align:right">'
                " masaldzhiyski</span></div></div>"
            )
        )
        .set_properties(**{"font-family": "Archivo", "font-size": "14px"})
        .apply_index(
            lambda x: np.where(
                x.isin(["1Y", "3Y", "10Y", "TREND"]),
                "text-align: center",
                "text-align: left",
            ),
            axis=1,
        )
        .apply_index(
            lambda x: np.where(x == "3Y", "color: blue !important", "color:black"),
            axis=1,
        )
        .set_table_attributes('style="border-spacing: 0px;"')
    )
    return df_result


def main():
    """Main function

    We read the data, create the summary table and style it
    The result is saved as an HTML file
    """
    df = pd.read_csv("./data.csv", thousands=",")
    df_graph = (
        df.groupby("Ticker")
        .apply(lambda x: produce_summary(x, x.name))
        .reset_index(drop=True)
    )
    df_result = style_table(df_graph)
    html = HTML(df_result.to_html())  # We can use Jinja2 if needed to render the HTML
    with open("result.html", "w") as f:
        f.write(html.data)


if __name__ == "__main__":
    main()
