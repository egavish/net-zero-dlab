#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  7 12:35:58 2022

@author: kmak
"""

import pandas as pd
import glob
import os
import plotly.express as px
from shapely.geometry.polygon import Polygon
import geopandas as gpd
from plotly.offline import plot, download_plotlyjs, init_notebook_mode, plot, iplot
import plotly.graph_objects as go
import shapely

filePath = '/Users/kmak/Desktop/EC.719/Building Energy Visualization/net-zero-dlab/Data files'

######
# Visualization
######

electricityData = pd.read_csv(filePath + '/Electricity.csv')
steamData = pd.read_csv(filePath + '/Steam.csv')
chilledWaterData = pd.read_csv(filePath + '/Chilled Water.csv')
buildingFootprints = pd.read_csv(filePath + '/building-footprint.csv')

steamData['geometry'] = gpd.GeoSeries.from_wkt(steamData['geometry'])

### Remove rows that do not have an associated building footprint
bad_indices = []
for i, row in steamData.iterrows():
    if type(row['geometry']) != Polygon:
        bad_indices.append(i)
steamData = steamData.drop(axis=0, labels=bad_indices)

# ### Reorder columns so geometry is second
# steamData = steamData.melt(id_vars=["BUILDING_NUMBER", "GEOMETRY"], 
#         var_name="Date", 
#         value_name="Steam Usage")

gdf = gpd.GeoDataFrame(steamData)
# print(gdf.columns)
#, geometry=steamData['GEOMETRY']).set_index("BUILDING_NUMBER")

month = '2010-02-01'

slider = list(steamData.columns)
slider.pop(0)
slider.pop(-1)

steps = []
for i in range(len(slider)):
    step = dict(method='restyle',
                args=['visible', [False] * len(slider)],
                label='{}'.format(i))
    step['args'][1][i] = True
    steps.append(step)

sliders = [dict(active=0, pad={"t": 1}, steps=steps)]

layout = dict(geo=gdf.geometry,
              sliders=sliders)
fig = dict(data=sliders, layout=layout) 

# figure = px.choropleth_mapbox(gdf,
#                           geojson=gdf.geometry,
#                           locations=gdf.index,
#                           color = gdf['2010-02-01'],
#                           color_continuous_scale='reds',
#                           # hover_over = gdf['2010-02-01'],
#                           mapbox_style='carto-positron',
#                           center={'lat':42.360001, 'lon':-71.092003},
#                           zoom=14,
#                           range_color=[0, 12000],
#                           animation_frame=slider
                          # )
px.offline.plot(fig, auto_open=True, image = 'png', image_filename="map_us_crime_slider" ,image_width=2000, image_height=1000, 
             filename='/your_path/map_us_crime_slider.html', validate=True)

# plot(figure)
# 


# NOTE: To covert str representation of Polygon to type Polygon
# electricityData['geometry'] = electricityData['geometry'].apply(shapely.wkt.loads)

#NOTE: To show plotly choropleth plots, I had to use plot(figure) instead of figure.show().
# It would then open in a browser window.

