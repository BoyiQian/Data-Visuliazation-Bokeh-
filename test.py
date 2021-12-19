from logging import log
from bokeh.layouts import column, gridplot, row
from bokeh.models.annotations import ColorBar, Legend, LegendItem, Title
from bokeh.models.glyphs import Circle
from bokeh.models.mappers import LinearColorMapper
from bokeh.models.sources import ColumnDataSource
from bokeh.models import CustomJS, Dropdown,ColumnDataSource
from bokeh.models.transforms import LinearInterpolator
from bokeh.palettes import Blues256, Colorblind, Magma256, Oranges, Turbo256, Viridis256, mpl,Spectral6,brewer
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
from bokeh.models import RadioButtonGroup,Legend

from math import pi

import pandas as pd

from bokeh.models import BasicTicker, ColorBar, LinearColorMapper, PrintfTickFormatter
from bokeh.plotting import figure, show
from bokeh.sampledata.unemployment1948 import data
print(data)
data['Year'] = data['Year'].astype(str)
data = data.set_index('Year')
data.drop('Annual', axis=1, inplace=True)
data.columns.name = 'Month'

years = list(data.index)
months = list(data.columns)

# reshape to 1D array or rates with a month and year for each row.
df = pd.DataFrame(data.stack(), columns=['rate']).reset_index()
print(df)
# this is the colormap from the original NYTimes plot
colors = ["#75968f", "#a5bab7", "#c9d9d3", "#e2e2e2", "#dfccce", "#ddb7b1", "#cc7878", "#933b41", "#550b1d"]
mapper = LinearColorMapper(palette=colors, low=df.rate.min(), high=df.rate.max())

TOOLS = "hover,save,pan,box_zoom,reset,wheel_zoom"

p = figure(title="US Unemployment ({0} - {1})".format(years[0], years[-1]),
           x_range=years, y_range=list(reversed(months)),
           x_axis_location="above", width=900, height=400,
           tools=TOOLS, toolbar_location='below',
           tooltips=[('date', '@Month @Year'), ('rate', '@rate%')])

p.grid.grid_line_color = None
p.axis.axis_line_color = None
p.axis.major_tick_line_color = None
p.axis.major_label_text_font_size = "7px"
p.axis.major_label_standoff = 0
p.xaxis.major_label_orientation = pi / 3

p.rect(x="Year", y="Month", width=1, height=1,
       source=df,
       fill_color={'field': 'rate', 'transform': mapper},
       line_color=None)

color_bar = ColorBar(color_mapper=mapper, major_label_text_font_size="7px",
                     ticker=BasicTicker(desired_num_ticks=len(colors)),
                     formatter=PrintfTickFormatter(format="%d%%"),
                     label_standoff=6, border_line_color=None)
p.add_layout(color_bar, 'right')

show(p)




# bokeh_doc=curdoc()
#
# file = "Video_Games_Sales_as_at_22_Dec_2016.csv"
# d = pd.read_csv(file)
#
# year_f = d["Year_of_Release"].dropna().unique().tolist()
# year_f = sorted(year_f)
# data = d[["Name", "Genre", "Year_of_Release", "NA_Sales","EU_Sales","JP_Sales","Other_Sales","Global_Sales"]]
# years = []
# for i in year_f:
#     years.append(str(int(i)))
# genre = d["Genre"].dropna().unique().tolist()
#
# menu2 =genre
#
# def callback(new):
#     if radio_button_group.active == 1:
#         layout =  row()
# radio_button_group = RadioButtonGroup(labels=menu2, active=0)
# radio_button_group.on_click(callback)
#
# label = ["North America", "European", "Japan", "Other"]
# region = ["NA_Sales", "EU_Sales", "JP_Sales", "Other_Sales"]
#
# source=dict()
# index = 0
# for i in label:
#     value = []
#     for j in years:
#         total1 = data[data["Year_of_Release"] == int(j)]["Global_Sales"].sum()
#         g1 = data[(data["Year_of_Release"] == int(j)) & (data["Genre"] == "Sports")]["Global_Sales"].sum()
#         denom = g1 / total1
#         total2 = data[(data["Year_of_Release"] == int(j)) & (data["Genre"] == "Sports")]["Global_Sales"].sum()
#         g2 = data[(data["Year_of_Release"] == int(j)) & (data["Genre"] == "Sports")][region[index]].sum()
#         nume = g2/total2
#
#         value.append(nume*denom)
#
#     source[i] = value
#     index += 1
#
# df = pd.DataFrame(source)
# print(df)
# p = figure()
# p.grid.minor_grid_line_color = '#eeeeee'
#
#
# p.varea_stack(stackers=label, x='index', color=brewer['Spectral'][len(region)], legend_label=label, source=df)
#
# p.legend.orientation = "horizontal"
# p.legend.background_fill_color = "#fafafa"
#
# show(p)
