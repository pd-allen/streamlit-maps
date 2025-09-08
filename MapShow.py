import leafmap.foliumap as leafmap

m = leafmap.Map()
cog_url = "HoogeIFFM_cog.tif"
cog_url2="HoogeWarDiary_cog.tif"
print(cog_url)
m.add_raster(cog_url)
m.add_raster(cog_url2)
m.to_streamlit(height=600)  # Use this in Streamlit