from typing import List, Dict, Literal
import requests
import datetime
import pandas
import matplotlib.pyplot as plt
import polyline
import geopy
import geopandas
import shapely
### 
# Step 0: Go to https://www.strava.com/settings/apps and make sure your map is not listed in the "My Apps" tab. If it is listed click revoke access to revoke access. This is necesary as we need to reauthorize it to create a new token with read_all permissions. 
# Step 1: Edit the URL below, replacing [Your Client Id Here] with the client id of your app. Then enter the URL below into your browser and hit enter
# https://www.strava.com/oauth/authorize?client_id=[Your Client Id Here]&response_type=code&redirect_uri=http://localhost/exchange_token&approval_prompt=force&scope=activity:read_all,read_all,profile:read_all
# Step 2: After hitting enter you should get a webpage error. This is correct and expected. Copy the new URL you get below: 
# http://localhost/exchange_token?state=&code=[Your Code Here]&scope=read,activity:read_all,profile:read_all,read_all
# Step 3: In the URL you just pasted above find the "code=[Your Code Here]" and put the code in the place below.
# Warning: It seems like you can only attempt this once per code, so if you get an error you must go back to Step 0, revoke access, and start again.
###
# client_id = '99657'
# client_secret = '15f516b9c11a1012cb946f137f989d3b83921af5'
# code = 'ba125514163624d8b9181fc28912d74797a14194'
# base_url = 'https://www.strava.com/oauth/token?'
# url = f"{base_url}client_id={client_id}&client_secret={client_secret}&code={code}&grant_type=authorization_code"
# url2 = "https://www.strava.com/oauth/token?client_id=99657&client_secret=15f516b9c11a1012cb946f137f989d3b83921af5&code=ba125514163624d8b9181fc28912d74797a14194&grant_type=authorization_code"
# data={}
# headers = {}

# response = requests.request("POST", url, headers=headers, data=data)

# print(response.text)
def get_access_token(client_id: int, client_secret: str, refresh_token: str) -> str:
	authorization_url = "https://www.strava.com/oauth/token"
	data = {
		'client_id': str(client_id),
    	'client_secret': client_secret,
    	'refresh_token': refresh_token,
    	'grant_type': "refresh_token",
    	'f': 'json'
		}
	res = requests.post(authorization_url, data=data)
	return res.json()['access_token']

def get_activities_for_year(year: int, access_token: str) -> List[dict]:
	start_of_year_epoch = datetime.datetime(year-1,12,30,0,0).timestamp()
	end_of_year_epoch = datetime.datetime(year+1,1,2,0,0).timestamp()
	activites_url = "https://www.strava.com/api/v3/athlete/activities"
	header = {'Authorization': 'Bearer ' + access_token}
	parameters = {'before':end_of_year_epoch, 'after':start_of_year_epoch, 'page': 1, 'per_page': 200}
	raw_activity_list = requests.get(activites_url, headers=header, params=parameters).json()
	activity_list = []
	for activity in raw_activity_list:
		if int(activity['start_date'][:4]) == year:
			activity_list.append(activity)
	return activity_list


client_id = 99657
client_secret = "15f516b9c11a1012cb946f137f989d3b83921af5"
refresh_token = "3084ecda19b970d28fca94b916cb3f44628ea8f6"

access_token = get_access_token(client_id,client_secret,refresh_token)
X = get_activities_for_year(2023,access_token)
print(len(X))

A = X[0]
path = A['map']['summary_polyline']
print(path)
L = polyline.decode(path,5)
print(len(L))

P = pandas.DataFrame(L)
P.columns = ['Lat','Long']
# print(P)

ls = shapely.LineString( P[['Long','Lat']].to_numpy() )
# line_gdf = geopandas.GeoDataFrame( [['101']],crs='epsg:4326', geometry=[ls] )
line_gdf = geopandas.GeoSeries(ls)
# Plot the lineString in red
# ax = line_gdf.plot(color="red", figsize=[4,10]);
# P.plot("Long", "Lat", kind="scatter", ax=ax);
# plt.show()

states_path = "tl_2022_us_state/tl_2022_us_state.shp"
df = geopandas.read_file(states_path)
df = df.to_crs("EPSG:4326")
georgia = df[df.STUSPS == 'GA']
michigan = df[df.STUSPS == 'MI']
ax = line_gdf.plot(color="red", figsize=[4,10]);
P.plot("Long", "Lat", kind="scatter", ax=ax);
georgia.plot(ax=ax)
plt.show()

print(line_gdf.length)
# print(line_gdf)
# print(georgia.geometry)
print(ls.intersects((georgia.geometry)))
# print(georgia.geometry)
# print(line_gdf.intersects((georgia.geometry),align=False))
# print(line_gdf.intersects((michigan.geometry),align=False))
# G = geopandas.GeoSeries(P,geometry=geopandas.points_from_xy(P.Long, P.Lat))

# print(G)

# world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))

# # We restrict to South America.
# ax = world[world.continent == 'North America'].plot(
#     color='white', edgecolor='black')

# # # We can now plot our ``GeoDataFrame``.
# G.plot(ax=ax, color='red')

# plt.show()

# df = pandas.DataFrame(
#     {'City': ['Buenos Aires', 'Brasilia', 'Santiago', 'Bogota', 'Caracas'],
#      'Country': ['Argentina', 'Brazil', 'Chile', 'Colombia', 'Venezuela'],
#      'Latitude': [-34.58, -15.78, -33.45, 4.60, 10.48],
#      'Longitude': [-58.66, -47.91, -70.66, -74.08, -66.86]})

# gdf = geopandas.GeoDataFrame(
#     df, geometry=geopandas.points_from_xy(df.Longitude, df.Latitude))
# print(gdf)
# world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))

# # We restrict to South America.
# ax = world[world.continent == 'South America'].plot(
#     color='white', edgecolor='black')

# # We can now plot our ``GeoDataFrame``.
# gdf.plot(ax=ax, color='red')

# plt.show()

# S = geopandas.GeoSeries([Point(1,1),Point(1,2)])
# print(S)

# geolocator = geopy.Nominatim(user_agent="test")
# for latLong in L[:100]:
# 	print(latLong)
# 	location = geolocator.reverse(latLong)
# 	address = location.raw['address']
# 	state = address.get('state', '')
# 	print(state)






