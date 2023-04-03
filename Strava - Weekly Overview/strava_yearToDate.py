from typing import List, Dict, Literal
import requests
import datetime
import pandas
import matplotlib.pyplot as plt
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

def date_from_iso_datetime(iso_date):
	return iso_date.split('T',1)[0]

def strava_date_to_weeknumber(strava_date):
	date = datetime.datetime.strptime(date_from_iso_datetime(strava_date),'%Y-%m-%d')
	return int(date.strftime('%W'))

def key_info_from_activity(activity: dict) -> dict:
	return {
		'date': date_from_iso_datetime(activity['start_date']),
		'week': strava_date_to_weeknumber(activity['start_date']),
		'type': activity['type'],
		'sport_type': activity['sport_type'],
		'distance': activity['distance'],
		'elevation_gain': activity['total_elevation_gain']
		}

def key_info_activity_list(activity_list: List[dict]) -> List[dict]:
	return [key_info_from_activity(activity) for activity in activity_list]

def activities_for_week(week_number: int, activity_list: List[dict]) -> List[dict]:
	return [activity for activity in activity_list if activity['week'] == week_number]

def convert_meters_to_feet(meters: float) -> float:
	return round(meters*3.28084,2)

def convert_meters_to_miles(meters: float) -> float:
	return round(meters*0.000621371,2)

Units = Literal["metric", "english"]

def totals_for_given_sport(sport_type: str, activity_list: list[dict], units: Units = "english") -> dict:
	distance = 0
	elevation_gain = 0
	for activity in activity_list:
		if activity['sport_type'] == sport_type:
			distance += activity['distance']
			elevation_gain += activity['elevation_gain']
	if units == "english":
		return {'distance': convert_meters_to_miles(distance), 'elevation_gain': convert_meters_to_feet(elevation_gain)}
	elif units == "metric":
		return {'distance': distance, 'elevation_gain': elevation_gain}


def overview_for_given_week(week_number: int, activity_list: List[dict], units: Units = "english") -> dict:
	activtiy_list_week = activities_for_week(week_number, activity_list)
	sport_types = set([activity['sport_type'] for activity in activtiy_list_week])
	weekly_totals = {}
	for sport in sport_types:
		weekly_totals[f"{sport.lower()}_elevation"] = (totals_for_given_sport(sport, activtiy_list_week, units))['elevation_gain']
		weekly_totals[f"{sport.lower()}_distance"] = (totals_for_given_sport(sport, activtiy_list_week, units))['distance']
	return  weekly_totals
	# return {sport: totalsForGivenSportType(sport, activtiy_list_week) for sport in sport_types}

def weekly_orverviews(activity_list: List[dict], units: Units = "english") -> dict:
	last_week_number = max([activity['week'] for activity in activity_list])
	return {week_number: overview_for_given_week(week_number, activity_list,units) for week_number in range(last_week_number + 1)}

def weekly_orverviews_Datafram(activity_list: List[dict], units: Units = "english") -> pandas.DataFrame:
	overview_dataframe = pandas.DataFrame(weekly_orverviews(activity_list, units)).transpose().fillna(0)
	index_level0 = [(column.split('_',1))[0] for column in overview_dataframe.columns]
	index_level1 = [(column.split('_',1))[1] for column in overview_dataframe.columns]
	multiindex = [index_level0,index_level1]
	overview_dataframe.columns = pandas.MultiIndex.from_arrays(multiindex)
	return overview_dataframe


client_id = 99657
client_secret = "15f516b9c11a1012cb946f137f989d3b83921af5"
refresh_token = "3084ecda19b970d28fca94b916cb3f44628ea8f6"

access_token = get_access_token(client_id,client_secret,refresh_token)
X = get_activities_for_year(2023,access_token)
print(len(X))


Y = key_info_activity_list(X)

Z = activities_for_week(13,Y)

print(pandas.DataFrame(Z))

W = overview_for_given_week(13,Y)
print(W)
#print(pandas.DataFrame(W))

U = weekly_orverviews(Y)
print(U)
df = weekly_orverviews_Datafram(Y)
with pandas.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
     print(df)

df.to_html('temp.html')
#
# df.plot.bar()
# plt.show()
# print(Y)

# dataFrame = pandas.DataFrame(Y)
# print(dataFrame)


