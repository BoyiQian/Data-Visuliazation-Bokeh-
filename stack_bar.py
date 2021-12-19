from logging import log
from bokeh.layouts import column, gridplot, row
from bokeh.models.annotations import ColorBar, Legend, LegendItem, Title
from bokeh.models.glyphs import Circle
from bokeh.models import CustomJS, Dropdown,ColumnDataSource, CheckboxGroup
from bokeh.models.transforms import LinearInterpolator
from bokeh.palettes import Blues256, Colorblind, Magma256, Oranges, Turbo256, Viridis256, mpl,Spectral6,viridis,turbo
from bokeh.transform import linear_cmap
from bokeh.models.widgets import Select,MultiSelect, Slider
from numpy import sqrt, square
import numpy as np
from numpy.core.arrayprint import format_float_positional
import pandas as pd
from bokeh.plotting import figure, output_file, show, curdoc,save
from bokeh.transform import cumsum
from math import pi
from bokeh.palettes import Category20c
from bokeh.models import RadioButtonGroup,Legend

file = "Video_Games_Sales_as_at_22_Dec_2016.csv"
d = pd.read_csv(file)
year_f = d["Year_of_Release"].dropna().unique().tolist()
year_f = sorted(year_f)
data = d[["Name", "Year_of_Release", "NA_Sales","EU_Sales","JP_Sales","Other_Sales","Global_Sales"]]
years = []
for i in year_f:
    years.append(str(int(i)))


bokeh_doc=curdoc()

menu = years
menu1 =["Overall", "Detail"]
def callback(new):
    plot, layout = creat_plot()
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

radio_button_group = RadioButtonGroup(labels=menu1, active=0)
radio_button_group.on_click(callback2)

checkbox_group = CheckboxGroup(labels=menu, active=[6,7,8,9])
checkbox_group.on_click(callback)

label = ["North America", "European", "Japan", "Other"]
region = ["NA_Sales", "EU_Sales", "JP_Sales", "Other_Sales"]

def creat_plot():

    years = []
    for i in checkbox_group.active:
        years.append(menu[i])
    colors = viridis(len(checkbox_group.active))

    source = dict()
    source["region"] = label
    for i in years:
        value =[]
        for j in region:
            value.append(data[data["Year_of_Release"] == int(i)][j].sum())
        source[i] = value



    plot = figure(title="sales number (in millions of units)", width=1000, height=800, x_range = label,
                  tools="hover",tooltips="$name @region: @$name")

    plot.vbar_stack(years, x="region", color = colors, width = 0.9, legend_label = years, source = source)

    layout = row(column(radio_button_group,checkbox_group), plot, creat_pie())

    return plot, layout

def creat_pie():
    years = []
    for i in checkbox_group.active:
        years.append(menu[i])
    plots = []
    for i in years:
        index = 0
        source = dict()
        for j in region:
            source[label[index]] = data[data["Year_of_Release"] == int(i)][j].sum()
            index += 1
        source1 = pd.Series(source).reset_index(name="value").rename(columns={'index': "region"})
        source1["angle"] = source1["value"] / source1["value"].sum() * 2 * pi
        source1["color"] = Category20c[len(region)]

        # source = ColumnDataSource(data=dict(label = label, sales =sales, color = Spectral6))
        # plot.xaxis.axis_label = select1.value
        # plot.yaxis.axis_label = select2.value
        title = "Pie Chart for Year " + i
        plot = figure(height=350, title=title, toolbar_location=None,
                      tools="hover", tooltips="@region: @value", x_range=(-0.5, 0.8))
        plot.wedge(x=0, y=1, radius=0.4, start_angle=cumsum('angle', include_zero=True), end_angle=cumsum("angle"),
                   line_color="white", fill_color='color', source=source1)

        plot.axis.axis_label = None
        plot.axis.visible = False
        plot.grid.grid_line_color = None
        plots.append(plot)

    plot = figure(height=350, x_range=(-0.5, 0.8))
    plot.wedge(x=0, y=1, radius=0, start_angle=cumsum('angle', include_zero=True), end_angle=cumsum("angle"),
               line_color="white", fill_color='color', legend_field="region", source=source1)
    plot.axis.axis_label = None
    plot.axis.visible = False
    plot.grid.grid_line_color = None
    plots.append(plot)
    grid = gridplot(plots, ncols=3, width=250, height=250)
    return grid

def create_mainplot():
    source = dict()
    index = 0
    for j in region:
        source[label[index]] = data[j].sum()
        index += 1

    source1 = pd.Series(source).reset_index(name="value").rename(columns={'index': "region"})

    source1["angle"] = source1["value"] / source1["value"].sum() * 2 * pi
    source1["color"] = mpl['Plasma'][len(region)]

    title = "global market(in millions of units)"
    plot = figure(height=1000, width=1000, title=title, toolbar_location=None,
                  tools="hover", tooltips="@region: @value")
    plot.wedge(x=0, y=1, radius=0.5, start_angle=cumsum('angle', include_zero=True), end_angle=cumsum("angle"),
               line_color="white", fill_color='color', source=source1, legend_group="region")
    plot.axis.axis_label = None
    plot.axis.visible = False
    plot.grid.grid_line_color = None
    plot.add_layout(plot.legend[0], "right")
    layout = row(radio_button_group, plot)
    return plot,layout

plot,layout =create_mainplot()

bokeh_doc.title = "line plots about genre"
bokeh_doc.add_root(layout)


