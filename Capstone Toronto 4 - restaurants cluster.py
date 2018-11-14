import pandas as pd
import numpy as np
import xlrd
import xlsxwriter
import sklearn
import regex
from sklearn.cluster import KMeans
import folium

toronto_venues = pd.read_excel(r'C:\Users\User01\Documents\Online Courses\IBM Data Science\Course  9 - Capstone\Main Project\toronto_venues.xlsx')

# List of food related places excluding shops but coffee shops:
list_food = ['Restaurant', 'Cafe', 'Coffee', 'Food', 'Bar', 'Pub', 'Bakery', 'Beer', 'Ice', 'Burger', 'Diner', 'Pizza', 'Steak', 'Sushi', 'Sandwich', 'Mexican', 'Italian', 'Breakfast']

df_food = toronto_venues

# Iterate through df_food and drop all venue categories that have nothing to do with food
for i, row in df_food.iterrows():

    if not regex.search(r'\L<list_food>', row['Venue Category'], list_food=list_food):
        df_food.drop([i], inplace=True)



# Prepare data frames for clustering. See which neighborhoods fall into different clusters based on
# their density of restaurants, bars, cafes etc.
num_cluster = 4

df_food_grouped = df_food.groupby('Neighborhood', as_index=False)['Venue Category'].count()

toronto_food_cluster = df_food_grouped.drop('Neighborhood', axis=1)

# Initiate clustering with k means
kmean_cluster = KMeans(n_clusters=num_cluster, random_state=0).fit(toronto_food_cluster)

df_cluster = toronto_food_cluster

df_cluster['Neighborhood'] = df_food_grouped['Neighborhood']

df_cluster['Cluster'] = kmean_cluster.labels_

df_cluster = df_cluster[['Neighborhood', 'Venue Category', 'Cluster']]

print(df_cluster.head())

#Save data frame with clusters as "food cluster neighbor.xlsx"
# Note: Other statistical data for each cluster can also be quickly evaluated in MS Excel
excel_cluster = pd.ExcelWriter(r'C:\Users\User01\Documents\Online Courses\IBM Data Science\Course  9 - Capstone\Main Project\food cluster neighbor.xlsx', engine='xlsxwriter')

df_cluster.to_excel(excel_cluster, sheet_name='Venue Category Clusters')

excel_cluster.save()
