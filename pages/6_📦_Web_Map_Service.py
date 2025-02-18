import os
os.system('pip install leafmap[maplibre]')
os.system('pip install openrouteservice')
import ast
import streamlit as st
import time
import geopandas as gpd
import leafmap.maplibregl as leafmap
import pandas as pd
import numpy as np
import openrouteservice
from openrouteservice import convert
import geojson
import json
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
'''
with row1_col2:

    esa_landcover = "https://services.terrascope.be/wms/v2"
    url = st.text_input(
        "Enter a WMS URL:", value="https://services.terrascope.be/wms/v2"
    )
    empty = st.empty()

    if url:
        options = get_layers(url)

        default = None
        if url == esa_landcover:
            default = "WORLDCOVER_2020_MAP"
        layers = empty.multiselect(
            "Select WMS layers to add to the map:", options, default=default
        )
        add_legend = st.checkbox("Add a legend to the map", value=True)
        if default == "WORLDCOVER_2020_MAP":
            legend = str(leafmap.builtin_legends["ESA_WorldCover"])
        else:
            legend = ""
        if add_legend:
            legend_text = st.text_area(
                "Enter a legend as a dictionary {label: color}",
                value=legend,
                height=200,
            )
'''
with row1_col1:
    
    client = openrouteservice.Client(key='5b3ce3597851110001cf62488f9235173eab4627b5f0ba01e928ef81')
    #fname='1stBttnCEF.xlsx'
    fname="8thHussarsItaly.xlsx"
    fn=fname[:len(fname)-5]
    print(fname,fn)
    fname= os.path.join(excelpath, fname)

    data =  pd.read_excel(fname,dtype={'Comments': str},na_values=[''])
    #print(data)
    data['color_column2']='blue'
    coordall=[data["Longitude"],data["Latitude"]]
    allcoord=[]
    coord1=[]
    for i, row in data.iterrows():
        coord1=[data["Longitude"][i],data["Latitude"][i]]
        allcoord.append(coord1)
        #print(i,data["Location"][i],coord1)
    #print(allcoord)
    coord2=tuple(allcoord)
    print(coord2)

    geometry = client.directions(coordinates=coord2,profile='foot-hiking',radiuses=[1000])['routes'][0]['geometry']
    #geometry = client.directions(coordinates=coord2,profile='driving-car',radiuses=[1000])['routes'][0]['geometry']
    #geometry = client.directions(coord2,profile="driving-car",format="geojson",radiuses=[1000])
    #print(geometry)
    decoded = convert.decode_polyline(geometry)
    #print(decoded)

 

    collection0=geojson.Feature(geometry=decoded)
    #print(collection0)
    collection ={"type":"FeatureCollection",
                 'features': [{"type": "Feature" ,
                 'geometry' :decoded,}]
    }
    features=[]
    features.append(geojson.Feature(geometry=decoded))
    feature_collection=geojson.FeatureCollection(features)
    #print(feature_collection)
    fnj=fn+'.geojson'
    fnj = os.path.join(jsonpath, fnj)

    print(fnj)
    with open(fnj, 'w') as outfile:
        json.dump(feature_collection, outfile)
 
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
