import numpy as np  # library to handle data in a vectorized manner
import json  # library to handle JSON files
from geopy.geocoders import Nominatim  # convert an address into latitude and longitude values
import requests  # library to handle requests
from pandas import json_normalize  # transform JSON file into a pandas data frame
import matplotlib.cm as cm
import matplotlib.colors as colors
from sklearn.cluster import KMeans
import folium  # map rendering library
import pandas as pd  # library for data analsysis
import wget
import os

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

url = "https://cocl.us/new_york_dataset"
file_path = "datasets/newyork_data.json"
if not os.path.isfile(file_path):
    wget.download(url=url, out=file_path)

with open(file_path) as json_data:
    newyork_data = json.load(json_data)

neighborhoods_data = newyork_data['features']
print(neighborhoods_data[0])
