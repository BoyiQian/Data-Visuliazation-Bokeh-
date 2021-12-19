import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from plotnine import *

# read file
file = "Video_Games_Sales_as_at_22_Dec_2016.csv"
d = pd.read_csv(file)
data = d[["Name", "Global_Sales","Critic_Score","User_Score"]]
data.sort_values(by="Global_Sales", inplace = True,ascending =False)
data = data.dropna()
data = data[:100]
p1 = ggplot(data, aes(x="Global_Sales",y="User_Score"))+geom_point()
print(p1)

p2 = ggplot(data, aes(x="Global_Sales",y="Critic_Score"))+geom_point()
print(p2)
