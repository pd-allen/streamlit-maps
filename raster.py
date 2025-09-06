import streamlit as st
import rasterio
from rasterio.plot import show
import matplotlib.pyplot as plt

# Path to the .tif file in your repository
tif_path = "HoogeIFFM.tif"            

# Open and display the TIFF
with rasterio.open(tif_path) as src:
    st.write(f"📊 Bands: {src.count}")
    st.write(f"📐 Dimensions: {src.width} x {src.height}")

    st.subheader("🖼️ TIFF Image Preview")
    fig, ax = plt.subplots()
    show(src, ax=ax)
    st.pyplot(fig)
