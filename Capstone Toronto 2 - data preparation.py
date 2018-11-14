import pandas as pd
import numpy as np
import xlrd



# Read the excel file with Toronto data from other python file:
toronto_venues = pd.read_excel(r'C:\Users\User01\Documents\Online Courses\IBM Data Science\Course  9 - Capstone\Main Project\toronto_venues.xlsx')

toronto_venues.head()

# Drop location data
venue_check = toronto_venues.drop(['Neighborhood Latitude', 'Neighborhood Longitude', 'Venue Latitude', 'Venue Longitude'], axis=1)

# Create different data frames based on grouping
to_venue_by_boro = venue_check.groupby('Neighborhood', as_index=False)['Venue','Venue Category'].agg(lambda x: len(x.value_counts()))
to_venue_by_boro.sort_values(by='Neighborhood')


to_venue_by_cat = venue_check.groupby('Venue Category', as_index=False)['Neighborhood'].agg(lambda x: len(x.value_counts()))
to_venue_by_cat.sort_values(by='Venue Category')


to_venue_by_venue = venue_check.groupby('Venue', as_index=False)['Neighborhood', 'Venue Category'].agg(lambda x: len(x.value_counts()))
to_venue_by_venue.sort_values(by='Venue')


to_groups_excel = pd.ExcelWriter(r'C:\Users\User01\Documents\Online Courses\IBM Data Science\Course  9 - Capstone\Main Project\toronto_groups.xlsx', engine='xlsxwriter')

# Export the grouped DataFrames to new excel file for later use or individual analysis in MS Excel.
to_venue_by_boro.to_excel(to_groups_excel, sheet_name='Neighborhood boroughs Overview')
to_venue_by_cat.to_excel(to_groups_excel, sheet_name='Venue Categories Overview')
to_venue_by_venue.to_excel(to_groups_excel, sheet_name='Venues Overview')

to_groups_excel.save()
