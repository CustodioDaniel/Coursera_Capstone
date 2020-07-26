import requests  # library to handle requests
import pandas as pd  # library for data analsysis
import numpy as np  # library to handle data in a vectorized manner
import random  # library for random number generation
from geopy.geocoders import Nominatim  # module to convert an address into latitude and longitude values
from IPython.display import Image
from IPython.core.display import HTML
from pandas import json_normalize
import folium  # plotting library
import webbrowser  # to display the maps on default Web browser (html)
from data.client_config import CLIENT_ID, CLIENT_SECRET

print('Folium installed')
print('Libraries imported.')

VERSION = '20180604'
LIMIT = 30
print('Your credentials: ')
print('CLIENT_ID: ' + CLIENT_ID)
print('CLIENT_SECRET:' + CLIENT_SECRET)

address = '102 North End Ave, New York, NY'

geolocator = Nominatim(user_agent="foursquare_agent")
location = geolocator.geocode(address)
latitude = location.latitude
longitude = location.longitude
print(latitude, longitude)

# Search for a specific venue category

search_query = 'Italian'
radius = 500
print(search_query + ' .... OK!')

url = 'https://api.foursquare.com/v2/venues/' \
      'search?client_id={}&client_secret={}&ll={},{}&v={}&query={}&radius={}&limit={}'.format(CLIENT_ID, CLIENT_SECRET,
                                                                                              latitude, longitude,
                                                                                              VERSION, search_query,
                                                                                              radius, LIMIT)
results = requests.get(url).json()
# assign relevant part of JSON to venues
venues = results['response']['venues']
# tranform venues into a dataframe
dataframe = json_normalize(venues)
# Display the DataFrame
desired_width = 320
pd.set_option('display.width', desired_width)
pd.set_option('display.max_columns', 10)
print(dataframe.head())

# Define information of interest and filter dataframe

# keep only columns that include venue name, and anything that is associated with location
filtered_columns = ['name', 'categories'] + [col for col in dataframe.columns if col.startswith('location.')] + ['id']
dataframe_filtered = dataframe.loc[:, filtered_columns]


# function that extracts the category of the venue
def get_category_type(row):
    try:
        categories_list = row['categories']
    except:
        categories_list = row['venue.categories']

    if len(categories_list) == 0:
        return None
    else:
        return categories_list[0]['name']


# filter the category for each row
dataframe_filtered['categories'] = dataframe_filtered.apply(get_category_type, axis=1)

# clean column names by keeping only last term
dataframe_filtered.columns = [column.split('.')[-1] for column in dataframe_filtered.columns]

print(dataframe_filtered)
print(dataframe_filtered.name)

venues_map = folium.Map(location=[latitude, longitude], zoom_start=13) # generate map centred around the Conrad Hotel

# add a red circle marker to represent the Conrad Hotel
folium.CircleMarker(
    [latitude, longitude],
    radius=10,
    color='red',
    popup='Conrad Hotel',
    fill = True,
    fill_color = 'red',
    fill_opacity = 0.6
).add_to(venues_map)

# add the Italian restaurants as blue circle markers
for lat, lng, label in zip(dataframe_filtered.lat, dataframe_filtered.lng, dataframe_filtered.categories):
    folium.CircleMarker(
        [lat, lng],
        radius=5,
        color='blue',
        popup=label,
        fill = True,
        fill_color='blue',
        fill_opacity=0.6
    ).add_to(venues_map)

# display map
venues_map.save("maps/italian_venues.html")
webbrowser.open("maps/italian_venues.html")

# Explore a Given Venue

venue_id = '4fa862b3e4b0ebff2f749f06' # ID of Harry's Italian Pizza Bar
url = 'https://api.foursquare.com/v2/venues/{}?client_id={}&client_secret={}&v={}'.format(venue_id, CLIENT_ID,
                                                                                          CLIENT_SECRET, VERSION)

result = requests.get(url).json()
print(result['response']['venue'].keys())

try:
    print(result['response']['venue']['rating'])
except:
    print('This venue has not been rated yet.')


venue_id = '4f3232e219836c91c7bfde94' # ID of Conca Cucina Italian Restaurant
url = 'https://api.foursquare.com/v2/venues/{}?client_id={}&client_secret={}&v={}'.format(venue_id, CLIENT_ID,
                                                                                          CLIENT_SECRET, VERSION)

result = requests.get(url).json()
try:
    print(result['response']['venue']['rating'])
except:
    print('This venue has not been rated yet.')

venue_id = '3fd66200f964a520f4e41ee3' # ID of Ecco
url = 'https://api.foursquare.com/v2/venues/{}?client_id={}&client_secret={}&v={}'.format(venue_id, CLIENT_ID,
                                                                                          CLIENT_SECRET, VERSION)

result = requests.get(url).json()
try:
    print(result['response']['venue']['rating'])
except:
    print('This venue has not been rated yet.')

# Get the number of tips
print(result['response']['venue']['tips']['count'])

# Get the venue's tips
# Ecco Tips
limit = 15  # set limit to be greater than or equal to the total number of tips
url = 'https://api.foursquare.com/v2/venues/{}/' \
      'tips?client_id={}&client_secret={}&v={}&limit={}'.format(venue_id, CLIENT_ID, CLIENT_SECRET, VERSION, limit)

results = requests.get(url).json()
tips = results['response']['tips']['items']
tip = results['response']['tips']['items'][0]
tip.keys()

# Format column width and display all tips
pd.set_option('display.max_colwidth', -1)
tips_df = json_normalize(tips) # json normalize tips
# columns to keep
filtered_columns = ['text', 'agreeCount', 'disagreeCount', 'id', 'user.firstName', 'user.lastName', 'user.gender', 'user.id']
tips_filtered = tips_df.loc[:, filtered_columns]
# display tips
print(tips_filtered)

# Search a Foursquare User

user_id = '484542633' # user ID with most agree counts and complete profile
url = 'https://api.foursquare.com/v2/users/' \
      '{}?client_id={}&client_secret={}&v={}'.format(user_id, CLIENT_ID, CLIENT_SECRET, VERSION)  # define URL

# send GET request
results = requests.get(url).json()
user_data = results['response']['user']

# display features associated with user
print(user_data.keys())
print('First Name: ' + user_data['firstName'])
print('Last Name: ' + user_data['lastName'])
print('Home City: ' + user_data['homeCity'])
print(user_data['tips'])

# Get User's tips
# define tips URL
url = 'https://api.foursquare.com/v2/users/{}/' \
      'tips?client_id={}&client_secret={}&v={}&limit={}'.format(user_id, CLIENT_ID, CLIENT_SECRET, VERSION, limit)

# send GET request and get user's tips
results = requests.get(url).json()
tips = results['response']['tips']['items']
tips_df = json_normalize(tips)
# filter columns
filtered_columns = ['text', 'agreeCount', 'disagreeCount', 'id']
tips_filtered = tips_df.loc[:, filtered_columns]
# display user's tips
print(tips_filtered)

# Let's get the venue for the tip with the greatest number of agree counts

tip_id = '5ab5575d73fe2516ad8f363b' # tip id
# define URL
url = 'http://api.foursquare.com/v2/tips/{}?client_id={}&client_secret={}&v={}'.format(tip_id, CLIENT_ID, CLIENT_SECRET, VERSION)
# send GET Request and examine results
result = requests.get(url).json()
print(result['response']['tip']['venue']['name'])
print(result['response']['tip']['venue']['location'])

# Get User's friends
user_friends = json_normalize(user_data['friends']['groups'][0]['items'])
# Retrieve the User's Profile Image
# 1. grab prefix of photo
# 2. grab suffix of photo
# 3. concatenate them using the image size
Image(url='https://igx.4sqi.net/img/user/300x300/'
          '484542633_mK2Yum7T_7Tn9fWpndidJsmw2Hof_6T5vJBKCHPLMK5OL-U5ZiJGj51iwBstcpDLYa3Zvhvis.jpg')

# Explore a location


