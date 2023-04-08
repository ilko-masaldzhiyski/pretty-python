import pandas as pd
import numpy as np
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
            ("text-align", "center"),
            ("padding-bottom", "10px"),
        ],
    },
    {
        "selector": ".square",
        "props": [
            ("padding", "5px"),
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

# Create a data frame with values. Scraped from AccuWeather
DATA = [
    {
        "day": 1,
        "icon": "heavy-snow",
        "low": 1,
        "high": 11,
        "dow": "Sat",
        "week_index": 1,
    },
    {
        "day": 2,
        "icon": "heavy-snow",
        "low": 0,
        "high": 11,
        "dow": "Sun",
        "week_index": 1,
    },
    {
        "day": 3,
        "icon": "partly-cloudy",
        "low": 0,
        "high": 10,
        "dow": "Mon",
        "week_index": 2,
    },
    {"day": 4, "icon": "snow", "low": -2, "high": 8, "dow": "Tue", "week_index": 2},
    {
        "day": 5,
        "icon": "heavy-snow",
        "low": -2,
        "high": 7,
        "dow": "Wed",
        "week_index": 2,
    },
    {
        "day": 6,
        "icon": "partly-cloudy",
        "low": -2,
        "high": 6,
        "dow": "Thu",
        "week_index": 2,
    },
    {
        "day": 7,
        "icon": "partly-cloudy",
        "low": -1,
        "high": 10,
        "dow": "Fri",
        "week_index": 2,
    },
    {
        "day": 8,
        "icon": "partly-cloudy",
        "low": 1,
        "high": 11,
        "dow": "Sat",
        "week_index": 2,
    },
    {"day": 9, "icon": "clouds", "low": 3, "high": 10, "dow": "Sun", "week_index": 2},
    {"day": 10, "icon": "rain", "low": 3, "high": 8, "dow": "Mon", "week_index": 3},
    {"day": 11, "icon": "clouds", "low": 3, "high": 13, "dow": "Tue", "week_index": 3},
    {"day": 12, "icon": "clouds", "low": 4, "high": 16, "dow": "Wed", "week_index": 3},
    {"day": 13, "icon": "sun", "low": 4, "high": 19, "dow": "Thu", "week_index": 3},
    {"day": 14, "icon": "sun", "low": 7, "high": 22, "dow": "Fri", "week_index": 3},
    {"day": 15, "icon": "sun", "low": 9, "high": 20, "dow": "Sat", "week_index": 3},
    {"day": 16, "icon": "rain", "low": 11, "high": 18, "dow": "Sun", "week_index": 3},
    {
        "day": 17,
        "icon": "partly-rainy",
        "low": 9,
        "high": 20,
        "dow": "Mon",
        "week_index": 4,
    },
    {"day": 18, "icon": "sun", "low": 10, "high": 13, "dow": "Tue", "week_index": 4},
    {"day": 19, "icon": "sun", "low": 11, "high": 16, "dow": "Wed", "week_index": 4},
    {"day": 20, "icon": "sun", "low": 7, "high": 19, "dow": "Thu", "week_index": 4},
    {
        "day": 21,
        "icon": "heavy-snow",
        "low": -2,
        "high": 9,
        "dow": "Fri",
        "week_index": 4,
    },
    {"day": 22, "icon": "clouds", "low": 1, "high": 12, "dow": "Sat", "week_index": 4},
    {
        "day": 23,
        "icon": "partly-cloudy",
        "low": 2,
        "high": 14,
        "dow": "Sun",
        "week_index": 4,
    },
    {
        "day": 24,
        "icon": "partly-rainy",
        "low": 3,
        "high": 14,
        "dow": "Mon",
        "week_index": 5,
    },
    {
        "day": 25,
        "icon": "partly-cloudy",
        "low": 4,
        "high": 15,
        "dow": "Tue",
        "week_index": 5,
    },
    {"day": 26, "icon": "rain", "low": 4, "high": 15, "dow": "Wed", "week_index": 5},
    {
        "day": 27,
        "icon": "partly-rainy",
        "low": 5,
        "high": 14,
        "dow": "Thu",
        "week_index": 5,
    },
    {
        "day": 28,
        "icon": "light-rain-with-thunder",
        "low": 5,
        "high": 11,
        "dow": "Fri",
        "week_index": 5,
    },
    {
        "day": 29,
        "icon": "heavy-rain",
        "low": 6,
        "high": 13,
        "dow": "Sat",
        "week_index": 5,
    },
    {
        "day": 30,
        "icon": "partly-rainy",
        "low": 6,
        "high": 14,
        "dow": "Sun",
        "week_index": 5,
    },
]


def style_cell(x: float) -> str:
    """Style the cells in the table

    Args:
        x (float): The value of the cell

    Returns:
        str: The HTML code to style the cell
    """
    if np.isnan(x):
        return '<img class="square" width=85px src="./images/square_light_blue.svg">'
    else:
        element = [e for e in DATA if e["day"] == x][0]
        icon = element["icon"]
        min = element["low"]
        max = element["high"]
        return (
            '<div style="position: relative;">'
            '<img class="square" width=85px src="./images/square_blue.svg"/>'
            f'<img style="position: absolute; top:25px; left:30px;" width=35px src="./images/{icon}.svg"/>'
            '<div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; text-align: center; vertical-align: bottom; font-weight: bold;">'
            f'<span style="position: absolute; top: 10px; left: 0; width: 100%; height: 100%; text-align: center; font-size: 12px; font-weight: bold; color: #007DFE;">{int(x)}</span>'
            "</div>"
            '<div style="position: absolute; top: 70px; left: 0; width: 100%; height: 100%; text-align: center; vertical-align: bottom; font-weight: bold;">'
            f'<span style="color: black; font-size:12px">{max}&deg; </span>'
            f'<span style="color: gray; font-size:8px">/{min}&deg;</span>'
            "</div>"
            "</div>"
        )


def style_table(df: pd.DataFrame) -> pd.DataFrame:
    """Style the table

    Args:
        df (DataFrame): The dataframe to style

    Returns:
        DataFrame: The styled dataframe
    """
    df_result = df.applymap(style_cell)
    MyStyler = Styler.from_custom_template(
        searchpath="", html_table="html_template.tpl"
    )
    styler = MyStyler(df_result)
    df_result = (
        styler.format()
        .hide()
        .set_table_styles(CUSTOM_STYLE)
        .set_caption(  # This would probably be better if added to the template
            (
                '<div style="padding-top: 20px; display: flex; justify-content:space-between">'
                '<div style="order: 1">'
                '<span style="text-align:left; display: inline; color: #787878;'
                'font-size: 12px;"> Source: <strong>AccuWeather</strong> | #30DayChartChallenge'
                " | Day 2</span></div>"
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
        .set_table_attributes(
            'style="border-spacing: 0px; margin-left: auto; margin-right: auto;"'
        )
    )
    return df_result


def main():
    """Main function"""
    df = pd.DataFrame(DATA)
    df_pivot = df.pivot(index="week_index", columns="dow", values="day").reset_index(
        drop=True
    )
    df_pivot = df_pivot[["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]]
    df_result = style_table(df_pivot)
    html = HTML(df_result.to_html())  # We can use Jinja2 if needed to render the HTML
    with open("result.html", "w") as f:
        f.write(html.data)


if __name__ == "__main__":
    main()
