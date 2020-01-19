#!/usr/bin/env python
# coding: utf-8

import requests
import json
import pandas as pd
import numpy as np
import datetime
from config import api_key
from config import google_key
import time

# Query the Yelp API for 1000 Restaurants in Minneapolis

data = []
headers = {'Authorization': 'Bearer %s' % api_key}
url='https://api.yelp.com/v3/businesses/search'

print('Downloading Yelp Data...',flush=True)

for offset in range(0, 1000, 50):
    
    params = {
        'limit':50, 
        'location':'Minneapolis, MN',

        'categories':'restaurants',
        'offset':offset
        }  
    
    response=requests.get(url, params=params, headers=headers)
    if response.status_code == 200:
        data += response.json()['businesses']
    elif response.status_code == 400:
        print('400 Bad Request')
        break
        
print(f'Yelp data downloaded...  There are {len(data)} records...',flush=True)

#Convert Yelp API data into a list of dictionaries to be converted into DataFrame

i=0
yelp_list=[]
for places in data:
    yelp_id=data[i]['id']
    name=data[i]['name']
    street=data[i]['location']['address1'] 
    city=data[i]['location']['city']
    zipcode=data[i]['location']['zip_code']
    address= f'{street}, {city} {zipcode}'
    rating=data[i]['rating']
    reviews=data[i]['review_count']
    latitude=data[i]['coordinates']['latitude']
    longitude=data[i]['coordinates']['longitude']
    if data[i]['is_closed']==False:
        business_dict={"YelpID":yelp_id,"Name":name,"Latitude":latitude,"Longitude":longitude,"Address":address, "Rating":rating,"Reviews":reviews}
        yelp_list.append(business_dict)
    i+=1
    
#Convert list of Yelp dictionaries into a DataFrame and save CSV file.

yelp_df=pd.DataFrame(yelp_list)
yelp_df=yelp_df[['YelpID','Name','Latitude','Longitude','Address','Rating','Reviews']]
yelp_df = yelp_df.drop_duplicates(subset=['Name','Address'])
yelp_df.to_csv("DataFiles/YelpData.csv")

print('Yelp DataFrame now stored in memory as "yelp_df" and csv "YelpData.csv" has been saved in DataFiles folder.',flush=True)
print(f'Removed duplicates. Leaving {len(yelp_df)} restaurants.')
print('---------------',flush=True)

#Match the 1000 items in Yelp list to the Google API and pull the same 1000 restaurants in Google.

print('Matching Yelp data list to Google API...   This will take some time, as we match each record...',flush=True)

url = 'https://maps.googleapis.com/maps/api/place/findplacefromtext/json?'
google_data=[]

for places in yelp_list:
    
    params = {
        'key':google_key,
        'input':places['Name'],
        'inputtype':'textquery',
        'locationbias': 'point:' + str(places['Latitude']) + ", " + str(places['Longitude']),
        'radius': 10,
        'fields':'name,formatted_address,place_id,geometry,rating,user_ratings_total'
        }
    
    response = requests.get(url, params=params)

    if len(response.json()['candidates'])>0:
        google_data.append(response.json()['candidates'][0])
    else:
        google_data.append("")

print(f'Google match has been completed...  There are {len(google_data)} records', flush=True)

#Convert Google API data to list to be converted to DataFrame

i=0
google_list=[]

for places in google_data:
    if places != "":
        if "place_id" in places:
            google_id = places['place_id']
        if "name" in places:
            name = places['name']
        if "formatted_address" in places:
            address = places['formatted_address']
        if "rating" in places:
            rating  = places['rating']
        if "user_ratings_total" in places:
            reviews = places['user_ratings_total']
        if "geometry" in places:
            latitude = places['geometry']['location']['lat']
            longitude = places['geometry']['location']['lng']
        business_dict = {"Google Places ID":google_id,"Name":name,"Latitude":latitude,"Longitude":longitude,"Address":address, "Rating":rating,"Reviews":reviews}
    
    else:
        business_dict = {"Google Places ID":"","Name":"","Latitude":"","Longitude":"","Address":"", "Rating":"","Reviews":""}
    
    google_list.append(business_dict)
    
    i+=1
    
#Convert list of Google entries to dataframe and save as csv.

google_df=pd.DataFrame(google_list)
google_df=google_df[google_df.Name != ""]
google_df=google_df[['Google Places ID','Name','Latitude','Longitude','Address','Rating','Reviews']]
google_df = google_df.drop_duplicates(subset=['Google Places ID'])
google_df.to_csv('DataFiles/GoogleData.csv')

print('Google DataFrame now stored in memory as "google_df" and csv "GoogleData.csv" has been saved in DataFiles folder.',flush=True)
print(f'Removed null and duplicate entries.  {len(google_df)} restaurants remain.')
print('---------------',flush=True)

#Create a list, DataFrame and CSV to compare Yelp and Google records.

i = 0
compare_list=[]

for i in range(len(google_list)):

    compare = {"Yelp":yelp_list[i]['Name'],"Google":google_list[i]['Name'],"GoogleAddress":google_list[i]['Address'],"Yelp Address":yelp_list[i]['Address']}
    compare_list.append(compare)
    i+=1

compare_df = pd.DataFrame(compare_list)
compare_df.to_csv('DataFiles/compare.csv')

print('"compare_df" has been stored in memory and csv "compare.csv" has been saved in DataFiles folder to allow easy comparison between Yelp and Google data.',flush=True)
print('---------------',flush=True)

#Match the 1000 items in Yelp list to the Minneapolis Health Code API and pull the inspection reports for the 1000 restaurants from yelp_list.

print('Matching Yelp data list to Minneapolis Health Inspection API...   This will take some time, as we match each record...',flush=True)

inspection_data=[]

for records in yelp_list:

    biz = records['Name']

    biz_string = biz.split(' ',1)[0].upper()
    biz_string = biz_string.replace("'","")
    biz_string = biz_string.replace("&","")

    url = 'https://services.arcgis.com/afSMGVsC7QlRK1kZ/arcgis/rest/services/Food_Inspections/FeatureServer/0/query?'

    minlat=records['Latitude']-.001
    maxlat=records['Latitude']+.001
    minlon=records['Longitude']-.001
    maxlon=records['Longitude']+.001

    params = f"where=BusinessName%20like%20'%25{biz_string}%25'%20AND%20Latitude%20%3E%3D%20{minlat}%20AND%20Latitude%20%3C%3D%20{maxlat}%20AND%20Longitude%20%3E%3D%20{minlon}%20AND%20Longitude%20%3C%3D%20{maxlon}"

    outfields = "&outFields=BusinessName,HealthFacilityIDNumber,FullAddress,InspectionType,DateOfInspection,InspectionIDNumber,InspectionScore,Latitude,Longitude&returnGeometry=false&outSR=4326"

    json = '&f=json'

    full_url = url+params+outfields+json

    response = requests.get(full_url)
    
    if response !="":
        inspection_data += response.json()['features']
    
print(f'Inspection data match has been completed...  There are {len(inspection_data)} records',flush=True)

#Convert Minneapolis inspection API data to list of inspection reports, convert to DataFrame, and save CSV.

inspection_data_list = []

for records in inspection_data:
    item = records['attributes']
    item['DateOfInspection']=time.strftime('%m/%d/%Y',time.gmtime(records['attributes']['DateOfInspection']/1000))
    inspection_data_list.append(item)
    
inspections_df = pd.DataFrame(inspection_data_list)
inspections_df = inspections_df.drop_duplicates(subset='InspectionIDNumber', keep='first')
inspections_df = inspections_df[['BusinessName','DateOfInspection','FullAddress','HealthFacilityIDNumber','InspectionIDNumber','InspectionScore','InspectionType','Latitude','Longitude']]
inspections_df.to_csv('DataFiles/InspectionsData.csv')

print('Inspections DataFrame now stored in memory as "inspections_df" and csv "InspectionsData.csv" has been saved in DataFiles folder.',flush=True)
print(f'There are {len(inspections_df)} unique inspections.')
print('---------------',flush=True)