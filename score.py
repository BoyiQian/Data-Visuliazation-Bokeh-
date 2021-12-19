from bokeh.models.annotations import ColorBar, Legend, LegendItem, Title
from bokeh.models.glyphs import Circle
from bokeh.layouts import column, gridplot, row
from bokeh.models import CustomJS, Dropdown,ColumnDataSource, CheckboxGroup
from bokeh.models.transforms import LinearInterpolator
from bokeh.models import CheckboxButtonGroup
from bokeh.palettes import Blues256, Colorblind, Magma256, Oranges, Category20,\
    Turbo256, Viridis256, mpl,Spectral6,viridis,turbo,Spectral,Plasma,inferno,Set3,all_palettes
from bokeh.transform import linear_cmap
from bokeh.models.widgets import Select,MultiSelect, Slider,RangeSlider,TextInput
from numpy import sqrt, square
import numpy as np
from numpy.core.arrayprint import format_float_positional
import pandas as pd

from bokeh.models import BasicTicker, ColorBar, LinearColorMapper, PrintfTickFormatter
import statistics
from bokeh.plotting import figure, output_file, show, curdoc
from bokeh.transform import cumsum
from math import pi
from bokeh.palettes import Category20c
from bokeh.models import RadioButtonGroup,Legend,SingleIntervalTicker

bokeh_doc=curdoc()
file = "Video_Games_Sales_as_at_22_Dec_2016.csv"
d = pd.read_csv(file)
d = d.dropna(subset=["Developer"])

year_f = d["Year_of_Release"].dropna().unique().tolist()
year_f = sorted(year_f)
d = d[["Name", "Genre","Year_of_Release", "Critic_Score", "Critic_Count","User_Score","User_Count","Developer","Global_Sales"]]
years = []
for i in year_f:
    years.append(str(int(i)))
genre = d["Genre"].dropna().unique().tolist()
developer = d["Developer"].unique().tolist()
d_s = dict()
for i in developer:
    d_s[i] = d[d["Developer"]==i]["Global_Sales"].sum()
d_s = sorted(d_s.items(),key = lambda i:i[1], reverse = True)

def callback(attr, old, new):
    layout.children[1]=create_plot()

def callback2(new):
    layout.children[1] = create_plot()

start=TextInput(title="start at top x-th developer (1-1963)", value = "1")
end=TextInput(title="end at top x-th developer (start-1963) ", value = "71")
start.on_change("value",callback)
end.on_change("value",callback)

menu = ["Year_of_Release","Genre"]
radio_button_group = RadioButtonGroup(labels=menu, active=0)
radio_button_group.on_click(callback2)

menu2 = ["Critic_Score", "Critic_Count","User_Score","User_Count","Global_Sales"]
select = Select(title = "value", options = menu2, value = "User_Score")
select.on_change("value",callback)



def create_plot():
    top_d = []
    for i in d_s[int(start.value)-1:int(end.value)]:
        top_d.append(i[0])
    if radio_button_group.active == 0:
        y_label = years
        title = "Developer's " + select.value +" on Year ({0} - {1})".format(y_label[0], y_label[-1])
    else:
        y_label = genre
        title = "Developer's " + select.value + " on different genre"


    y = []
    x_developer = []
    value = []
    data = d.drop(d[d[select.value] == "tbd"].index)
    data = data.dropna(subset=[select.value])
    for i in top_d:
        for j in y_label:
            x_developer.append(i)
            y.append(j)
            if radio_button_group.active == 0:
                j = int(j)
            s = data[(data["Developer"] == i) & (data[menu[radio_button_group.active]] == j)][select.value].tolist()
            s = list(map(float, s))
            if len(s) == 0:
                value.append(0)
            else:
                value.append(statistics.mean(s))

    low = np.unique(value)[1]

    source = pd.DataFrame({"year": y, "developer": x_developer, "data": value})
    colors = ["#75968f", "#a5bab7", "#c9d9d3", "#e2e2e2", "#dfccce", "#ddb7b1", "#cc7878", "#933b41", "#550b1d"]
    mapper = LinearColorMapper(palette=Viridis256, low=low, high=source.data.max(), low_color='#cccccc')

    TOOLS = "hover,save,pan,box_zoom,reset,wheel_zoom"

    p = figure(title=title,
               x_range=top_d, y_range=y_label,
               x_axis_location="above", width=1400, height=1000,
               tools=TOOLS, toolbar_location='below',
               tooltips=[('Developer', '@developer'), (menu[radio_button_group.active], '@year'), (select.value, '@data')])

    p.grid.grid_line_color = None
    p.axis.axis_line_color = None
    p.axis.major_tick_line_color = None
    p.axis.major_label_text_font_size = "7px"
    p.axis.major_label_standoff = 0
    p.xaxis.major_label_orientation = pi / 3

    p.rect(x="developer", y="year", width=1, height=1,
           source=source,
           fill_color={'field': 'data', 'transform': mapper},
           line_color=None)

    color_bar = ColorBar(color_mapper=mapper, major_label_text_font_size="7px",
                         ticker=BasicTicker(desired_num_ticks=len(colors)),
                         formatter=PrintfTickFormatter(format="%d"),
                         label_standoff=6, border_line_color=None)
    p.add_layout(color_bar, 'right')
    return p

layout = row(column(start,end,radio_button_group,select),create_plot())

bokeh_doc.title = "heat map about developers"

bokeh_doc.add_root(layout)
# print(genre)
# print(years)
