import pandas as pd
import numpy as np
from typing import Tuple
from IPython.display import HTML
from pandas.io.formats.style import Styler

CUSTOM_STYLE = [
    # Table column headers
    {
        "selector": "th:not(.index_name)",
        "props": [
            ("background-color", "white"),
            ("color", "#2f2f2f"),
            ("font-size", "16px"),
            ("font-weight", "bold"),
            ("font-family", "Archivo"),
        ],
    },
    # Color bars for different medals
    {
        "selector": ".color_bars",
        "props": [
            ("position", "absolute"),
            ("top", "50%"),
            ("transform", "translate(-50%, -50%)"),
        ],
    },
    # Medals header
    {
        "selector": ".header_medals",
        "props": [
            ("padding-left", "10px"),
            ("padding-right", "70px"),
            ("position", "relative"),
            ("top", "-6px"),
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
    # Every 2nd table row
    {
        "selector": "tr:nth-child(even)",
        "props": [
            ("background-color", "#f2f2f2"),
            ("border", "1px solid #f2f2f2 !important"),
        ],
    },
    # Table data
    {
        "selector": "td",
        "props": [
            ("color", "#2f2f2f"),
            ("font-size", "18px"),
            ("white-space", "nowrap"),
            ("font-family", "Archivo"),
        ],
    },
]


def prepare_data(
    df: pd.DataFrame, df_pop: pd.DataFrame
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Prepare data for plotting.

    Args:
        df (pd.DataFrame): Dataframe with Olympic medal data.
        df_pop (pd.DataFrame): Dataframe with population data.

    Returns:
        Tuple[pd.DataFrame, pd.DataFrame]: Dataframes with prepared data.
    """
    df = df[
        ["countries ", "winter_gold", "winter_silver", "winter_bronze", "winter_total"]
    ].copy()
    df.rename(columns={"countries ": "country"}, inplace=True)
    df.loc[df["country"] == "Germany", "winter_gold"] = df.loc[
        df["country"].str.contains("Germany"), "winter_gold"
    ].sum()
    df.loc[df["country"] == "Germany", "winter_silver"] = df.loc[
        df["country"].str.contains("Germany"), "winter_silver"
    ].sum()
    df.loc[df["country"] == "Germany", "winter_bronze"] = df.loc[
        df["country"].str.contains("Germany"), "winter_bronze"
    ].sum()
    df.loc[df["country"] == "Germany", "winter_total"] = df.loc[
        df["country"].str.contains("Germany"), "winter_total"
    ].sum()

    df_pop = df_pop[["Country/Territory", "2022 Population"]].copy()
    df_pop.rename(columns={"Country/Territory": "country"}, inplace=True)
    df_pop.loc[df_pop["country"] == "United Kingdom", "country"] = "Great Britain"
    return df, df_pop


def merge_data(df: pd.DataFrame, df_pop: pd.DataFrame) -> pd.DataFrame:
    """Merge dataframes with Olympic medal data and population data.

    Args:
        df (pd.DataFrame): Dataframe with Olympic medal data.
        df_pop (pd.DataFrame): Dataframe with population data.

    Returns:
        pd.DataFrame: Dataframe with merged data.
    """
    df_geo = df.merge(how="left", right=df_pop, on="country")
    df_geo.loc[df_geo["country"] == "Soviet Union", "2022 Population"] = 241730819
    df_geo.sort_values(by="winter_gold", ascending=False, inplace=True)
    df_geo = df_geo.head(10).copy()
    df_geo.reset_index(drop=True, inplace=True)
    df_geo["2022 Population"] = df_geo["2022 Population"].astype(int)
    return df_geo


def add_html(df: pd.DataFrame) -> pd.DataFrame:
    """Add HTML code to dataframe.

    Args:
        df (pd.DataFrame): Dataframe with merged data.

    Returns:
        pd.DataFrame: Dataframe with HTML code.
    """
    df["flag"] = df.apply(
        lambda x: f'<img style="max-height:50px; max-width:50px;" src="images/{x["country"]}.svg"/>',
        axis=1,
    )
    df["medals"] = df.apply(
        lambda x: (
            '<div style="text-align:left; position:relative">'
            f'<img style="max-height: 30px;" width={1.7*x["winter_gold"]}px src="images/Gold.png"/>'
            f'<img style="max-height: 30px;" width={1.7*x["winter_silver"]}px src="images/Silver.png"/>'
            f'<img style="max-height: 30px; padding-right: 50px" width={1.7*x["winter_bronze"]}px src="images/Bronze.png"/>'
            f'<div class="color_bars" style="color: #2f2f2f; left: {1.7*(x["winter_gold"]/2)}px;">{x["winter_gold"]}</div>'
            f'<div class="color_bars" style="color: #e2e2e2; left: {1.7*(x["winter_gold"] + x["winter_silver"]/2)}px;">{x["winter_silver"]}</div>'
            f'<div class="color_bars" style="color: #ffffff; left: {1.7*(x["winter_gold"] + x["winter_silver"] + x["winter_bronze"]/2)}px;">{x["winter_bronze"]}</div>'
            "</div>"
        ),
        axis=1,
    )
    df["Population<br>size"] = df.apply(
        lambda x: f'<img style="max-height:50px; max-width:50px;" width={5+45*x["2022 Population"]/338289857}px src="images/Circle.svg"/>',
        axis=1,
    )
    df = df[["country", "flag", "medals", "winter_total", "Population<br>size"]].rename(
        columns={
            "country": "",
            "flag": " ",
            "medals": (
                '<div style="text-align:center; position: relative">'
                '<img width=25px src="images/Gold.png"/><span class="header_medals">Gold</span>'
                '<img width=25px src="images/Silver.png"/><span class="header_medals">Silver</span>'
                '<img width=25px src="images/Bronze.png"/><span class="header_medals">Bronze</span>'
                "</div>"
            ),
            "winter_total": "Total<br>amount",
        }
    )
    return df


def style_table(df: pd.DataFrame) -> pd.DataFrame:
    """Style dataframe.

    Args:
        df (pd.DataFrame): Dataframe with HTML code.

    Returns:
        pd.DataFrame: Styled dataframe.
    """
    MyStyler = Styler.from_custom_template(
        searchpath="", html_table="html_template.tpl"
    )
    styler = MyStyler(df)
    df_result = (
        styler.format()
        .hide()
        .set_table_styles(CUSTOM_STYLE)
        .set_properties(
            subset=["Total<br>amount"],
            **{"text-align": "center", "padding-right": "20px"},
        )
        .set_properties(
            subset=[""],
            **{
                "padding": "20px",
            },
        )
        .set_properties(
            subset=[" "],
            **{
                "padding-right": "20px",
            },
        )
        .set_properties(
            subset=["Population<br>size"],
            **{
                "text-align": "center",
            },
        )
        .apply_index(
            lambda x: np.where(
                x == "Total<br>amount",
                "padding-right: 20px",
                "font-family: Archivo",
            ),
            axis=1,
        )
        .set_caption(  # This would probably be better if added to the template
            (
                '<div style="display: flex; justify-content:space-between">'
                '<div style="order: 1">'
                '<span style="text-align:left; display: inline; color: #787878;'
                'font-size: 12px;"> Source: <strong>Kaggle</strong> | W14 pretty-python'
                "</span></div>"
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
        .set_table_attributes('style="border-spacing: 0px;"')
    )
    return df_result


def main():
    """Main function."""

    df = pd.read_csv("olympic_stats.csv", thousands=",")
    df_pop = pd.read_csv("world_population.csv")
    df, df_pop = prepare_data(df, df_pop)
    df_geo = merge_data(df, df_pop)
    df_geo = add_html(df_geo)
    df_result = style_table(df_geo)
    html = HTML(df_result.to_html())
    with open("result.html", "w") as f:
        f.write(html.data)


if __name__ == "__main__":
    main()
