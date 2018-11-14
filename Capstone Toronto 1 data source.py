import requests
import pandas as pd
import numpy as np
import xlrd
import xlsxwriter
from bs4 import BeautifulSoup


# Function to call Foursquare App and assign found venues to Neighborhoods and boroughs
def getNearbyVenues(names, latitudes, longitudes, radius=500):

    venues_list=[]
    for name, lat, lng in zip(names, latitudes, longitudes):

        # URL of respective Foursquare App
        url = 'https://api.foursquare.com/v2/venues/explore?&client_id={}&client_secret={}&v={}&ll={},{}&radius={}&limit={}'.format(
            CLIENT_ID,
            CLIENT_SECRET,
            VERSION,
            lat,
            lng,
            radius,
            Limit)

        # Results from Foursquare
        results = requests.get(url).json()['response']['groups'][0]['items']


        # Values to return
        venues_list.append([(
            name,
            lat,
            lng,
            v['venue']['name'],
            v['venue']['location']['lat'],
            v['venue']['location']['lng'],
            v['venue']['categories'][0]['name']) for v in results])

    nearby_venues = pd.DataFrame([item for venue_list in venues_list for item in venue_list])
    nearby_venues.columns = ['Neighborhood',
                  'Neighborhood Latitude',
                  'Neighborhood Longitude',
                  'Venue',
                  'Venue Latitude',
                  'Venue Longitude',
                  'Venue Category']

    return(nearby_venues)


# Define constants for Foursquare URL
CLIENT_ID = 'STUXIOFXH55TITYVUTGKIDG3CAG50XD0B3SM2XE2WWB3IU1Q'
CLIENT_SECRET = 'AU3QRD5UCY5MRYBX3K2E3MMBOGCVNTA2WMHPZTDEN4IJ4CLZ'
VERSION = '20180605'
Limit = 100

# Get Toronto location data from Wikipedia:

wiki_url = requests.get('https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M').text

soup = BeautifulSoup(wiki_url,'lxml')
print(soup.prettify())

wiki_table = soup.find_all('table',{'class':'wikitable sortable'})
table = wiki_table[0]

header_row = table.find('tr')
col_names = []


content = []
temp_post =[]
temp_boro = []
temp_neighbor = []

# Iterate through wikipedia HTML text and get values
for tr in table.find_all('tr'):

    temp_list =[]

    td_all = tr.find_all('td')

    if not td_all:
        continue

    post, boro, neighbor = [td.text.strip() for td in td_all[0:3]]

    temp_list.append(post)
    temp_list.append(boro)
    temp_list.append(neighbor)

    content.append(temp_list)


# Assign columns names to new df
df_toronto = pd.DataFrame(data=content, columns=['PostalCode', 'Borough', 'Neighborhood'])

df_toronto = df_toronto[df_toronto.Borough != 'Not assigned']

# Save df as "toronto_original.xlsx"
writer = pd.ExcelWriter(r'C:\Users\User01\Documents\Online Courses\IBM Data Science\Course  9 - Capstone\Main Project\toronto_original', engine='xlsxwriter')

df_toronto.to_excel(writer)

writer.save()

# Read df with coordinates and merge with toronto postal data
df_geo = pd.read_csv(r'C:\Users\User01\Documents\Online Courses\IBM Data Science\Course  9 - Capstone\Main Project\Geospatial_Toronto.csv')

df_geo.rename(columns={'Postal Code':'PostalCode'}, inplace=True)

df_torontoGEO = pd.merge(df_toronto, df_geo,how='left', on='PostalCode')

# Toronto venues from Foursquare
toronto_venues = getNearbyVenues(names=df_torontoGEO['Neighborhood'], latitudes=df_torontoGEO['Latitude'], longitudes=df_torontoGEO['Longitude'])

# Save nw df with venues as "toronto_venues.xlsx"
toronto_excel = pd.ExcelWriter(r'C:\Users\User01\Documents\Online Courses\IBM Data Science\Course  9 - Capstone\Main Project\toronto_venues.xlsx', engine='xlsxwriter')

toronto_venues.to_excel(toronto_excel, sheet_name='Toronto Venues')

toronto_excel.save()
