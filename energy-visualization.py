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
from plotly.offline import plot
import plotly.graph_objects as go
import shapely

filePath = '/Users/kmak/Desktop/EC.719/Building Energy Visualization'

######
# Visualization
######

electricityData = pd.read_csv(filePath + '/Electricity.csv')
steamData = pd.read_csv(filePath + '/Steam.csv')
chilledWaterData = pd.read_csv(filePath + '/Chilled Water.csv')
buildingFootprints = pd.read_csv(filePath + '/building-footprint.csv')

# NOTE: To covert str representation of Polygon to type Polygon
# electricityData['geometry'] = electricityData['geometry'].apply(shapely.wkt.loads)

#NOTE: To show plotly choropleth plots, I had to use plot(figure) instead of figure.show().
# It would then open in a browser window.







