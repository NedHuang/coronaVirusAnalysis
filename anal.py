import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns



#reading data from the csv file
data1 = pd.read_csv("COVID19_line_list_data.csv")
data2 = pd.read_csv("time_series_covid_19_confirmed.csv")
print(data2.shape)
print(data2[1])