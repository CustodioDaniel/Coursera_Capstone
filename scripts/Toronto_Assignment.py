import pandas as pd
import geocoder

df = pd.read_html('https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M')[0]
desired_width = 320
pd.set_option('display.width', desired_width)
pd.set_option('display.max_columns', 10)
print(df.head())
# Keep only Postal Codes with assigned Boroughs
df = df[df.Borough != 'Not assigned']
# Reset the index of the data frame
df.index = pd.RangeIndex(len(df.index))
print(df.head())

# # with geocoder
# for index, postal_code in zip(df.index, df['Postal Code']):
#     # initialize your variable to None
#     lat_lng_coords = None
#
#     # loop until you get the coordinates
#     while lat_lng_coords is None:
#         g = geocoder.google('{}, Toronto, Ontario'.format(postal_code))
#         lat_lng_coords = g.latlng
#
#     latitude = lat_lng_coords[0]
#     longitude = lat_lng_coords[1]
#     df.loc[index, 'Latitude'] = latitude
#     df.loc[index, 'Longitude'] = longitude

# with csv file
df_latlong = pd.read_csv('datasets/Geospatial_Coordinates.csv')
print(df_latlong.head())
for index, postal_code in zip(df.index, df['Postal Code']):

    lat_lng_coords = df_latlong.loc[df_latlong['Postal Code'] == postal_code, ['Latitude', 'Longitude']]
    df.loc[index, 'Latitude'] = lat_lng_coords.iloc[0, 0]
    df.loc[index, 'Longitude'] = lat_lng_coords.iloc[0, 1]

print(df.head())
