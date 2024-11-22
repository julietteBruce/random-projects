import openrouteservice
from bs4 import BeautifulSoup
import requests
import re 
import json
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import numpy as np
import pandas as pd

### Gets HTML of website at given URL via BeautifulSoup
def get_webpage(url):
	req = requests.get(url)
	return BeautifulSoup(req.content, 'html.parser')


### Returns list of instutions of speakers at AMS Sectional from given URL
def get_speakersInstutions(url):
	soup = get_webpage(url)
	## This finds all of the speakers tags as speakers are marked with a *
	speakers = soup.find_all('strong',string=re.compile(r'[*]'))
	## The instituion is located oustide the strong tag so we get it via next_sibling
	institutions = [item.next_sibling for item in speakers]
	## Cleaing things up by deleting commas and leading/trailing spaces
	return [item.replace(', ','').strip() for item in institutions]


stateAb = [ 'AL', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL', 'GA',
           'IA', 'ID', 'IL', 'IN', 'KS', 'KY', 'LA', 'MA', 'MD', 'ME',
           'MI', 'MN', 'MO', 'MS', 'MT', 'NC', 'ND', 'NE', 'NH', 'NJ', 'NM',
           'NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX',
           'UT', 'VA', 'VT', 'WA', 'WI', 'WV', 'WY']

statesISO = ['US-'+state for state in stateAb]

def onlyCertainStates(address,states):
	placeISO = address.raw['address']['ISO3166-2-lvl4']
	return placeISO in states


def get_speakerGPS(place):
	geolocator = Nominatim(user_agent="geoapiExercises",timeout=10)
	address = geolocator.geocode(place,country_codes="us",addressdetails=True)
	if address is not None: 
		if onlyCertainStates(address,statesISO) == True:
			return [place,address.latitude ,address.longitude]
		else:
			return [place,None,None]
	else:
		return [place,None,None]

def get_allSpeakersGPS(url):
	institutions = get_speakersInstutions(url)
	return [get_speakerGPS(place) for place in institutions]

### Returns driving duration (seconds) and distance (meters) between two Lat-Long points
def get_drivingInfo(local1,local2):
	## Opens client
	client = openrouteservice.Client(key='5b3ce3597851110001cf6248b96ddff4d6e84ff9918d080865cbd84f')
	cords = (local1,local2)
	## Makes API request for directions
	f = client.directions(cords,radiuses=[5000])
	## Accesses summary to get distance and duration info.
	duration = f['routes'][0]['summary']['duration']
	distance = f['routes'][0]['summary']['distance']
	return [duration,distance]

def get_speakerDrivingInfo(place,hostCord):
	if place[1] is not None:
		speakerCord = (place[2],place[1])
		drivingInfo = get_drivingInfo(speakerCord,hostCord)
		return drivingInfo
	else:
		return [None,None]


def get_speakerGeoDistance(place,hostCord):
	if place[1] is not None:
		speakerCord = (place[1],place[2])
		print((speakerCord,hostCord))
		return [geodesic(speakerCord,hostCord).km]
	else:
		return [None]

def get_allSpeakerAllInfo(url,host):
	hostAddress = get_speakerGPS(host)
	hostCord = (hostAddress[2],hostAddress[1])
	hostCordGEO = (hostAddress[1],hostAddress[2])
	print(hostCord)
	allInstitutions = get_allSpeakersGPS(url)
	data = []
	for place in allInstitutions:
		print(place)
		driving = get_speakerDrivingInfo(place,hostCord)
		geo  = get_speakerGeoDistance(place,hostCordGEO)
		entry = place+driving+geo
		print(entry)
		data.append(entry)
	return data


def sectional_DataFram(url,host):
	data = get_allSpeakerAllInfo(url,host)
	return pd.DataFrame(data,columns=['location','latitude', 'longitude','driving duration','driving distance','geoDistance'])


def sectional_Save_DataFram(url,host,name):
	df = sectional_DataFram(url,host)
	strg = 'Output_'+name+'.csv'
	df.to_csv(strg)


#get_webpage('https://www.ams.org/meetings/sectional/2296_progfull.html')
#get_speakersInstutions('https://www.ams.org/meetings/sectional/2296_progfull.html')
#test = get_allSpeakersGPS('https://www.ams.org/meetings/sectional/2296_progfull.html')
#print(test)
#print(get_drivingInfo((-80.278,36.134),(-85.296,35.045)))
sectional_Save_DataFram('https://www.ams.org/meetings/sectional/2266_progfull.html','University of California, Riverside, Riverside, CA','UCR_FW19')
#geolocator = Nominatim(user_agent="geoapiExercises",timeout=10)
#address = geolocator.geocode('University Of Hawaii',country_codes="us",addressdetails=True)
#print(address.raw.keys())
#print(address.raw['address']['ISO3166-2-lvl4'])
#print(get_speakerGPS('University of Hawaii'))