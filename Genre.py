from logging import log
from bokeh.layouts import column, gridplot, row
from bokeh.models.annotations import ColorBar, Legend, LegendItem, Title
from bokeh.models.glyphs import Circle
from bokeh.models import CustomJS, Dropdown,ColumnDataSource, CheckboxGroup
from bokeh.models.transforms import LinearInterpolator
from bokeh.models import CheckboxButtonGroup
from bokeh.palettes import Blues256, Colorblind, Magma256, Oranges, Category20,\
    Turbo256, Viridis256, mpl,Spectral6,viridis,turbo,Spectral,Plasma,inferno,Set3,all_palettes
from bokeh.transform import linear_cmap
from bokeh.models.widgets import Select,MultiSelect, Slider
from numpy import sqrt, square
import numpy as np
from numpy.core.arrayprint import format_float_positional
import pandas as pd
from bokeh.plotting import figure, output_file, show, curdoc
from bokeh.transform import cumsum
from math import pi
from bokeh.palettes import Category20c
from bokeh.models import RadioButtonGroup,Legend,SingleIntervalTicker

file = "Video_Games_Sales_as_at_22_Dec_2016.csv"
d = pd.read_csv(file)
d = d.dropna(subset=["Genre"])
year_f = d["Year_of_Release"].dropna().unique().tolist()
year_f = sorted(year_f)
data = d[["Name", "Genre", "Year_of_Release", "NA_Sales","EU_Sales","JP_Sales","Other_Sales","Global_Sales"]]
years = []
for i in year_f:
    years.append(str(int(i)))
genre = d["Genre"].dropna().unique().tolist()
# print(genre)
# print(years)

bokeh_doc=curdoc()

menu = years
menu1 = ["Overall", "Detail"]
menu2 =genre
def callback(new):
    plot, layout = create_mainplot()
    bokeh_doc.clear()
    bokeh_doc.title = "years stack bar plot"
    bokeh_doc.add_root(layout)

def callback2(new):
    if radio_button_group.active == 0:
        plot, layout = create_mainplot()
        bokeh_doc.clear()
        bokeh_doc.title = "years stack bar plot"
        bokeh_doc.add_root(layout)
    else:
        plot, layout = creat_plot()
        bokeh_doc.clear()
        bokeh_doc.title = "years stack bar plot"
        bokeh_doc.add_root(layout)


# def callback3(new):
#     plot, layout = create_mainplot()
#     bokeh_doc.clear()
#     bokeh_doc.title = "years stack bar plot"
#     bokeh_doc.add_root(layout)

radio_button_group = RadioButtonGroup(labels=menu2, active=0)
radio_button_group.on_click(callback)


radio_button_group = RadioButtonGroup(labels=menu1, active=0)
radio_button_group.on_click(callback2)

radio_button_group2 = RadioButtonGroup(labels=menu2, active=0)
radio_button_group2.on_click(callback2)

checkbox_button_group = CheckboxButtonGroup(labels=menu2, active=[0,1,2])
checkbox_button_group.on_click(callback)

label = ["North America", "European", "Japan", "Other"]
region = ["NA_Sales", "EU_Sales", "JP_Sales", "Other_Sales"]

def creat_plot():
    bokeh_doc.theme="caliber"
    source = dict()
    index = 0
    for i in label:
        value = []
        for j in years:
            total1 = data[data["Year_of_Release"] == int(j)]["Global_Sales"].sum()
            g1 = data[(data["Year_of_Release"] == int(j)) & (data["Genre"] == genre[radio_button_group2.active])]["Global_Sales"].sum()
            denom = g1 / total1
            total2 = data[(data["Year_of_Release"] == int(j)) & (data["Genre"] == genre[radio_button_group2.active])]["Global_Sales"].sum()
            g2 = data[(data["Year_of_Release"] == int(j)) & (data["Genre"] == genre[radio_button_group2.active])][region[index]].sum()
            nume = g2 / total2
            value.append(nume * denom)

        source[i] = value
        index += 1

    df = pd.DataFrame(source)

    plot = figure(title="percentage for each genre in every region changing by year",width=1200, height=1100, tools="hover")
    plot.grid.minor_grid_line_color = '#eeeeee'
    plot.varea_stack(stackers=label, x='index', color=all_palettes['Viridis'][len(region)], legend_label=label, source=df)
    plot.legend.orientation = "horizontal"
    # plot.legend.background_fill_color = "#fafafa"
    # plot.grid_line_color = None
    plot.xaxis.axis_label = "Year (start from 1980)"
    layout = row(radio_button_group,column(radio_button_group2, plot))
    return plot,layout

def create_mainplot():
    bokeh_doc.theme = 'dark_minimal'
    plot = figure(title="percentage for each genre changing by year",width=1200, height=1100, tools="hover")
    source = dict()
    color = Category20[len(genre)]
    index = 0
    for i in checkbox_button_group.active:
        y = []
        for j in years:
            total = data[data["Year_of_Release"] == int(j)] ["Global_Sales"].sum()
            g = data[(data["Year_of_Release"] == int(j)) & (data["Genre"] == genre[i])]["Global_Sales"].sum()
            y.append(g/total)
        plot.line(years,y,legend_label=genre[i],color = color[index], line_width =3, hover_color='white', hover_alpha=0.5)
        index += 1
    plot.xaxis.ticker = SingleIntervalTicker(interval=1)
    layout = row(radio_button_group,column(checkbox_button_group, plot))

    return plot,layout

plot,layout = create_mainplot()

bokeh_doc.title = "years stack bar plot"
bokeh_doc.theme = 'dark_minimal'
bokeh_doc.add_root(layout)


