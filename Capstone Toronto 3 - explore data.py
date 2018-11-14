import pandas as pd
import numpy as np
import xlrd
import folium
import json

path_to_groups = r'C:\Users\User01\Documents\Online Courses\IBM Data Science\Course  9 - Capstone\Main Project\toronto_groups.xlsx'

# Data to create geographical charts
to_geojson = r'C:\Users\User01\Documents\Online Courses\IBM Data Science\Course  9 - Capstone\Main Project\toronto_crs84.geojson'
to_lat = 43.653908
to_long = -79.384293

# Read Excel data into dataframes again
# Note: If data was sorted or changed in MS Excel, pandas might return wrong results due to mixed indices
# Therefore, each index has been removed from excel files and is re-apllied when read into pandas
to_venue_by_boro = pd.read_excel(path_to_groups, sheet_name='Neighborhood boroughs Overview')
to_venue_by_cat = pd.read_excel(path_to_groups, sheet_name='Venue Categories Overview')
to_venue_by_venue = pd.read_excel(path_to_groups, sheet_name='Venues Overview')

# Borough with most categories:
i_max = to_venue_by_boro['Venue Category'].idxmax()
print('The neighborhood with most different categories: ',to_venue_by_boro['Neighborhood'].iloc[i_max])

# The most common venue category in boroughs:
i_max = to_venue_by_cat['Neighborhood'].idxmax()
print('The most common category: ',to_venue_by_cat['Venue Category'].iloc[i_max])

# The most common venue name:
i_max = to_venue_by_venue['Neighborhood'].idxmax()
print('The most common venue name: ', to_venue_by_venue['Venue'].iloc[i_max])


# Back to the main data frame:

# Create choropleth chart for some Toronto areas.
# Note: Geojson file and key_on feature of map prone to errors
to_geojson = r'C:\Users\User01\Documents\Online Courses\IBM Data Science\Course  9 - Capstone\Main Project\toronto2.geojson'

toronto_data = pd.read_excel(r'C:\Users\User01\Documents\Online Courses\IBM Data Science\Course  9 - Capstone\Main Project\toronto_venues.xlsx')

# Load data from geojson found on internet
geo = read_json = json.load(open(to_geojson))

df_to_choro = toronto_data.groupby(['Neighborhood'], as_index=False)['Venue'].agg(lambda x: len(x.value_counts()))

# Creat map from folium with threshold
to_map = folium.Map(location=[to_lat, to_long], zoom_start=10, tiles='Mapbox bright')

threshold_scale_1 = np.linspace(df_to_choro['Venue'].min(),
                              df_to_choro['Venue'].max(),
                              6, dtype=int)

# Create choropleth map
# Note: Due to differences in data from Foursquare and geojson, choropleth map might be prone to errors
to_map.choropleth(
    geo_data=geo,
    name='to_choropleth',
    data=df_to_choro,
    columns=['Neighborhood', 'Venue'],
    key_on='feature.properties.name',
    fill_color='BuGn',
    fill_opacity=0.7,
    line_opacity=0.3,
    threshold_scale=threshold_scale_1)

to_map

