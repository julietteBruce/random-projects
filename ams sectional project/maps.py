import geopandas as gpd
from shapely.geometry import Point, Polygon
import pandas as pd
import matplotlib.pyplot as plt

pd.set_option('display.max_columns',None,'display.max_rows',None)

shape_path = '/Users/juliettebruce/Desktop/cb_2018_us_state_5m/cb_2018_us_state_5m.shp'

shape = gpd.read_file(shape_path)
print(shape)

df = pd.read_csv ('/Users/juliettebruce/Desktop/Output_UTC_FSE22.csv')
print(df)
crs="EPSG:4326"
# zip x and y coordinates into single feature
geometry = [Point(xy) for xy in zip(df['longitude'], df['latitude'])]
print(geometry)
# create GeoPandas dataframe. NOTE THE EXCEPTION HAPPENS HERE
geo_df = gpd.GeoDataFrame(df,
 crs = crs,
 geometry = geometry)

shape = shape.dropna()
shape = shape[~shape['NAME'].isin(['Hawaii', 'United States Virgin Islands','Guam','Puerto Rico',
	'Commonwealth of the Northern Mariana Islands','American Samoa','Alaska'])]
ax = shape.boundary.plot(edgecolor='black',linewidth=0.5, figsize=(10, 5))
shape.plot(ax=ax,facecolor="none")

#df.plot(ax=ax, kind = 'scatter', x = 'longitude', y = 'latitude')
geo_df.plot(column='driving duration',ax=ax,alpha=0.75, legend=True,markersize=10)

ax.get_xaxis().set_visible(False)
ax.get_yaxis().set_visible(False)

for edge in ['right', 'bottom', 'top','left']:
    ax.spines[edge].set_visible(False)

plt.show()

print(df)