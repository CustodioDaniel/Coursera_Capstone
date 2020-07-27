import pandas as pd
import geocoder

# # initialize your variable to None
# lat_lng_coords = None
#
# # loop until you get the coordinates
# while(lat_lng_coords is None):
#   g = geocoder.google('{}, Toronto, Ontario'.format(postal_code))
#   lat_lng_coords = g.latlng
#
# latitude = lat_lng_coords[0]
# longitude = lat_lng_coords[1]

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
