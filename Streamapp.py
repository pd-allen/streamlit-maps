import streamlit as st
import leafmap.foliumap as leafmap

st.set_page_config(layout="wide")
st.title("🌍 GeoTIFF Viewer")

# Sidebar for user input
with st.sidebar:
    st.header("Settings")
    tif_file = st.text_input("Enter path to your GeoTIFF file", "your_file.tif")
    colormap = st.selectbox("Choose a colormap", ["terrain", "viridis", "plasma", "gray", "inferno"])

# Create the map
m = leafmap.Map(center=[45.4215, -75.6998], zoom=10)

# Add the raster layer
if tif_file:
    try:
        m.add_raster(tif_file, layer_name="GeoTIFF Layer", colormap=colormap)
    except Exception as e:
        st.error(f"Error loading TIFF: {e}")

# Display the map
m.to_streamlit(height=600)