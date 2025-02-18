import os
os.system('pip install leafmap[maplibre]')
#os.system('pip install openrouteservice')
import ast
import streamlit as st
import time
import geopandas as gpd
import leafmap.foliumap as leafmap
import pandas as pd
import numpy as np
#import openrouteservice
#from openrouteservice import convert
#import geojson
#import json
import os.path
from os import path
import requests
mappath="c:\python\data\maps"
excelpath="c:\python\data\excel"
imagespath="c:\python\data\images"
htmlpath="c:\python\data\html"
jsonpath="c:\python\data\json"


st.set_page_config(layout="wide")

markdown = """
A Streamlit map template
<https://github.com/opengeos/streamlit-map-template>
"""

st.sidebar.title("About")
st.sidebar.info(markdown)
logo = "https://i.imgur.com/UbOXYAU.png"
st.sidebar.image(logo)


@st.cache_data
def get_layers(url):
    options = leafmap.get_wms_layers(url)
    return options


st.title("Web Map Service (WMS)")
st.markdown(
    """
This app is a demonstration of loading Web Map Service (WMS) layers. Simply enter the URL of the WMS service
in the text box below and press Enter to retrieve the layers. Go to https://apps.nationalmap.gov/services to find
some WMS URLs if needed.
"""
)

row1_col1, row1_col2 = st.columns([3, 1.3])
width = None
height = 600
layers = None

    
#client = openrouteservice.Client(key='5b3ce3597851110001cf62488f9235173eab4627b5f0ba01e928ef81')
#fname='1stBttnCEF.xlsx'
#fname="8thHussarsItaly.xlsx"
#fname ="https://raw.githubusercontent.com/opengeos/data/main/world/world_cities.csv"
fname= 'https://raw.githubusercontent.com/pd-allen/pd-allen.github.io/main/docs/8thHussarsItaly.xlsx'
#fn=fname[:len(fname)-5]
#print(fname,fn)
#fname= os.path.join(excelpath, fname)
#data= leafmap.csv_to_df(fname)
data =  pd.read_excel(fname,dtype={'Comments': str},na_values=[''])
#print(data)
# data['color_column2']='blue'
print(data['Longitude'][14])
#m = leafmap.Map(center=[data['Longitude'][14],data['Latitude'][14]], zoom=14)
#m = leafmap.Map(center=(13.6,41.5),layers_control=True, zoom=8)
m = leafmap.Map(center=(41.6,13.6), layers_control=True,color_column=False,zoom=8)
#m.add_points_from_xy(data, x="longitude", y="latitude",color="red",popup=["name","country"],layer_name='points')
m.add_points_from_xy(data, x="Longitude", y="Latitude",color="red",popup=["Location","Date", "Comments"],layer_name='points')

url='https://raw.githubusercontent.com/pd-allen/pd-allen.github.io/main/docs/8thHussarsItaly.json'

print(url)
gdf = gpd.read_file(url)
coordinates = list(gdf.geometry[0].coords)
print(coordinates[:5])     
source = {
    "type": "geojson",
    "data": {
        "type": "Feature",
        "geometry": {"type": "LineString", "coordinates": [coordinates[0]]},
    },
}
m.add_source("trace", source)
layer = {
    "id": "trace",
    "type": "line",
    "source": "trace",
    "paint": {"line-color": "red", "line-opacity": 0.75, "line-width": 5},
}
m.add_layer(layer)
#m.jump_to({"center": coordinates[0], "zoom": 14})
m.set_pitch(60)
paint_line = {
    "line-color": "red",
    "line-width": 4,
}
m.add_geojson(url,layer_type="line", paint=paint_line, name="blocks-line")
m.add_basemap("OpenTopoMap")

m.to_streamlit(width, height)


