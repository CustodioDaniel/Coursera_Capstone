import requests  # library to handle requests
import pandas as pd  # library for data analsysis
import numpy as np  # library to handle data in a vectorized manner
import random  # library for random number generation
from geopy.geocoders import Nominatim  # module to convert an address into latitude and longitude values
from IPython.display import Image
from IPython.core.display import HTML
from pandas.io.json import json_normalize
import folium  # plotting library

print('Folium installed')
print('Libraries imported.')

CLIENT_ID = 'your-client-ID'  # your Foursquare ID
CLIENT_SECRET = 'your-client-secret'  # your Foursquare Secret

VERSION = '20180604'
LIMIT = 30
print('Your credentials: ')
print('CLIENT_ID: ' + CLIENT_ID)
print('CLIENT_SECRET:' + CLIENT_SECRET)
