import geopandas as gpd
from shapely.geometry import Point, Polygon
import pandas as pd
import matplotlib.pyplot as plt

pd.set_option('display.max_columns',None,'display.max_rows',None)

df = pd.read_csv ('/Users/juliettebruce/Desktop/Output_UTC_FSE22.csv')
print(df)

print(len(df.index))
print(len(df[df['latitude'].isnull()]))
dff = df[df['latitude'].notna()]

dff.hist(column='driving distance',bins=20)
plt.show()