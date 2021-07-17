#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from warnings import filterwarnings
filterwarnings('ignore')


# In[2]:


df=pd.read_csv('D:\Zomato_spatial\zomato.csv')
df.head()


# In[3]:


df.isna().sum()


# In[4]:


df.dropna(axis='index',subset=['location'],inplace=True)


# In[5]:


df.isna().sum()


# In[6]:


len(df['location'].unique())


# In[8]:


locations=pd.DataFrame({"Name":df['location'].unique()})


# In[9]:


locations.head()


# In[4]:


from geopy.geocoders import Nominatim


# In[5]:


geolocator=Nominatim(user_agent="app")


# In[6]:


'''lat_lon=[]
for location in locations['Name']:
    location = geolocator.geocode(location)
    if location is None:
        lat_lon.append(np.nan)
    else:    
        geo=(location.latitude,location.longitude)
        lat_lon.append(geo)'''


# In[10]:


lat=[]
lon=[]
for location in locations['Name']:
    location = geolocator.geocode(location)    
    if location is None:
        lat.append(np.nan)
        lon.append(np.nan)
    else:
        lat.append(location.latitude)
        lon.append(location.longitude)


# In[11]:


print(lat,lon)


# In[12]:


locations['lat']=lat
locations['lon']=lon


# In[13]:


locations.head()


# In[20]:


locations.to_csv('D:\Zomato_spatial/zomato_locations.csv',index=False)


# #### We have found out latitude and longitude of each location listed in the dataset using geopy
# #### This is used to plot maps.

# In[14]:


Rest_locations=pd.DataFrame(df['location'].value_counts().reset_index())


# In[15]:


Rest_locations.columns=['Name','count']
Rest_locations.head()


# #### now combine both the dataframes

# In[16]:


locations.shape


# In[17]:


Rest_locations.shape


# In[18]:


Restaurant_locations=Rest_locations.merge(locations,on='Name',how="left").dropna()
Restaurant_locations.head()


# In[17]:


Restaurant_locations['count'].max()

!pip install folium
# In[29]:


def generateBaseMap(default_location=[12.93, 77.62], default_zoom_start=12):
    base_map = folium.Map(location=default_location, zoom_start=default_zoom_start)
    return base_map


# In[30]:


import folium
from folium.plugins import HeatMap
basemap=generateBaseMap()


# In[31]:


basemap


# In[32]:


Restaurant_locations[['lat','lon','count']]


# #### Heatmap of Bengalore Restaurants

# In[33]:


HeatMap(Restaurant_locations[['lat','lon','count']],zoom=20,radius=15).add_to(basemap)


# In[34]:


basemap

It is clear that restaurants tend to concentrate in central bangalore area.
The clutter of restaurants lowers are we move away from central.
So,potential restaurant entrepreneurs can refer this and find out good locations for their venture.
note heatmap is good when we have latitude,longitude or imporatnce of that particular place or count of that place¶
# In[35]:


from folium.plugins import FastMarkerCluster


# In[36]:


FastMarkerCluster(data=Restaurant_locations[['lat','lon','count']].values.tolist()).add_to(basemap)
basemap


# #### Heat Map: where are the restaurants with high average rate?

# In[37]:


df.head()


# In[38]:


len(df['location'].unique())


# In[39]:


df['rate'].unique()


# In[40]:


df.dropna(axis=0,subset=['rate'],inplace=True)


# In[30]:


df['rate'].unique()


# In[41]:


def split(x):
    return x.split('/')[0]


# In[42]:


df['rating']=df['rate'].apply(split)


# In[43]:


df['rating'].unique()


# In[44]:


df.replace('NEW',0,inplace=True)


# In[45]:


df.replace('-',0,inplace=True)


# In[46]:


df.head()


# In[47]:


df.dtypes


# In[48]:


df['rating']=pd.to_numeric(df['rating'])


# In[49]:


df['rating'].dtype


# In[50]:


df.groupby(['location'])['rating'].mean().sort_values(ascending=False)


# In[51]:


df.groupby(['location'])['rating'].mean()


# In[52]:


avg_rating=df.groupby(['location'])['rating'].mean().values


# In[53]:


avg_rating


# In[54]:


loc=df.groupby(['location'])['rating'].mean().index
loc


# In[55]:


geolocator=Nominatim(user_agent="app")


# In[56]:


lat=[]
lon=[]
for location in loc:
    location = geolocator.geocode(location)    
    if location is None:
        lat.append(np.nan)
        lon.append(np.nan)
    else:
        lat.append(location.latitude)
        lon.append(location.longitude)


# In[57]:


rating=pd.DataFrame()


# In[58]:


rating['location']=loc
rating['lat']=lat
rating['lon']=lon
rating['avg_rating']=avg_rating


# In[59]:


rating.head()


# In[60]:


rating.isna().sum()


# In[61]:


rating=rating.dropna()


# In[63]:


HeatMap(rating[['lat','lon','avg_rating']],zoom=20,radius=15).add_to(basemap)
basemap


# ### Above are the restaurants with high average rate

# #### Heatmap of North Indian restaurants

# In[65]:


df.head()


# In[66]:


df2= df[df['cuisines']=='North Indian']
df2.head()


# In[67]:


north_india=df2.groupby('location')['url'].count().reset_index()
north_india.columns=['Name','count']
north_india.head()


# In[68]:


north_india=north_india.merge(locations,on="Name",how='left').dropna()


# In[69]:


north_india.head()


# In[70]:


basemap=generateBaseMap()
HeatMap(north_india[['lat','lon','count']].values.tolist(),zoom=20,radius=15).add_to(basemap)
basemap


# #### Automate Above Stuffs, & create for South India, & many other zones

# In[71]:


def Heatmap_Zone(zone):
    df3=df[df['cuisines']==zone]
    df_zone=df3.groupby(['location'],as_index=False)['url'].agg('count')
    df_zone.columns=['Name','count']
    df_zone=df_zone.merge(locations,on="Name",how='left').dropna()
    basemap=generateBaseMap()
    HeatMap(df_zone[['lat','lon','count']].values.tolist(),zoom=20,radius=15).add_to(basemap)
    return basemap


# In[72]:


df['cuisines'].unique()


# In[73]:


Heatmap_Zone('South Indian')

As for the visualization in the current date- 17/07/2021, It can be visaluzed that in current pandemic situation Zomato is mostly active in central Bengaluru city.
Still most of the hotels have shutted their online delivery off as due to infection concern,
It can be visualized through heatmarker that Someshwaranagar is having most active Zomato availed Hotels who are delivering.