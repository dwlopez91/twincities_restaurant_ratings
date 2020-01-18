#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import json
import pandas as pd
import numpy as np
import datetime
from config import api_key
from config import google_key
import sqlalchemy
import urllib
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import PrimaryKeyConstraint
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.schema import Sequence


# In[2]:


data = []

headers = {'Authorization': 'Bearer %s' % api_key}

url='https://api.yelp.com/v3/businesses/search'

print('Downloading Yelp Data...')

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
        
print(f'Yelp data downloaded...  There are {len(data)} records...')


# In[3]:


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
    
print('yelp_list with needed data has been built.')


# In[4]:


yelp_df=pd.DataFrame(yelp_list)
yelp_df['Index']=yelp_df.index
yelp_df=yelp_df[['Index','YelpID','Name','Latitude','Longitude','Address','Rating','Reviews']]
yelp_df.to_csv("DataFiles/YelpData.csv")

print('Yelp DataFrame now stored in memory as "yelp_df" and csv "YelpData.csv" has been saved in DataFiles folder.')
print('---------------')


# In[5]:


print('Matching Yelp data list to Google API...   This will take some time, as we match each record...')

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

print(f'Google match has been completed...  There are {len(google_data)} records')


# In[6]:


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
        if "reviews" in places:
            reviews = places['user_ratings_total']
        if "geometry" in places:
            latitude = places['geometry']['location']['lat']
            longitude = places['geometry']['location']['lng']
        business_dict = {"Google Places ID":google_id,"Name":name,"Latitude":latitude,"Longitude":longitude,"Address":address, "Rating":rating,"Reviews":reviews}
    
    else:
        business_dict = {"Google Places ID":"","Name":"","Latitude":"","Longitude":"","Address":"", "Rating":"","Reviews":""}
    
    google_list.append(business_dict)
    
    i+=1
    
print('google_list with needed data has been built.')


# In[7]:


google_df=pd.DataFrame(google_list)
google_df.to_csv('DataFiles/GoogleData.csv')


print('Google DataFrame now stored in memory as "google_df" and csv "GoogleData.csv" has been saved in DataFiles folder.')
print('---------------')


# In[8]:


i - 0
compare_list=[]
yelpgeo_list=[]

for i in range(len('yelp_list')):

    compare = {"Yelp":yelp_list[i]['Name'],"Google":google_list[i]['Name'],"GoogleAddress":google_list[i]['Address'],"Yelp Address":yelp_list[i]['Address']}
    compare_list.append(compare)
    i+=1

compare_df = pd.DataFrame(compare_list)
compare_df.to_csv('DataFiles/compare.csv')

print('"compare_df" has been stored in memory and csv "compare.csv" has been saved in DataFiles folder to allow easy comparison between Yelp and Google data.')
print('---------------')


# In[9]:


print('Matching Yelp data list to Minneapolis Health Inspection API...   This will take some time, as we match each record...')

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

    outfields = "&outFields=BusinessName,OBJECTID,HealthFacilityIDNumber,RiskLevel,FullAddress,InspectionType,InspectionResult,DateOfInspection,InspectionIDNumber,YearOfInspection,InspectionScore,Latitude,Longitude,ZipCode,ViolationStatus&returnGeometry=false&outSR=4326"

    json = '&f=json'

    full_url = url+params+outfields+json

    response = requests.get(full_url)
    
    if response !="":
        inspection_data += response.json()['features']
    
print(f'Inspection data match has been completed...  There are {len(inspection_data)} records')


# In[10]:


inspection_data_list = []

for records in inspection_data:
    item = records['attributes']
    inspection_data_list.append(item)
    
print('inspection_data_list with needed data has been built.')


# In[11]:


inspections_df = pd.DataFrame(inspection_data_list)
inspections_df
inspections_df.to_csv('DataFiles/InspectionsData.csv')

print('Inspections DataFrame now stored in memory as "inspections_df" and csv "InspectionsData.csv" has been saved in DataFiles folder.')
print('---------------')


# In[12]:

