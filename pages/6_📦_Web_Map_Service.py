import os
os.system('pip install leafmap[maplibre]')
#os.system('pip install openrouteservice')
import ast
import streamlit as st
import time
import geopandas as gpd
import leafmap.maplibregl as leafmap
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

with row1_col1:
    
    #client = openrouteservice.Client(key='5b3ce3597851110001cf62488f9235173eab4627b5f0ba01e928ef81')
    #fname='1stBttnCEF.xlsx'
    #fname="8thHussarsItaly.xlsx"
    fname= 'https://pd-allen.github.io/doc/8thHussarsItaly.xlsx'
    fn=fname[:len(fname)-5]
    print(fname,fn)
    #fname= os.path.join(excelpath, fname)

    data =  pd.read_excel(fname,dtype={'Comments': str},na_values=[''])
    #print(data)
    data['color_column2']='blue'

    m = leafmap.Map(center=(50.0,3.0), layers_control=True,color_column=False,zoom=8)

    m.add_points_from_xy(data, x="Longitude", y="Latitude",color="red",popup=["Location","Date", "Comments"],layer_name='points')
    m
    #fn ="test_collection.geojson"
    m.add_geojson(fnj,layer_name='routename',style = {
            "stroke": True,
            "color": 'blue',
            "weight": 4,
            "opacity": 1,
            "fill": False,
            "fillColor": "#0000ff",
            "fillOpacity": 0.1,
        })

    m.add_basemap("OpenTopoMap")
    m.to_streamlit(width, height)
