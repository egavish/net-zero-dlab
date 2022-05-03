#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 12 17:23:34 2022

@author: kmak
"""


import pandas as pd
import glob
import os
import plotly.express as px
from shapely.geometry.polygon import Polygon
import numpy as np

filePath = '/Users/kmak/Desktop/EC.719/Building Energy Visualization/net-zero-dlab/Data files' ##change to your filename
inputSignifier = 'input_energy_data-*.csv'


######
# Reorganizing building energy usage csv files
######


joined_files = os.path.join(filePath, inputSignifier)
joined_list = glob.glob(joined_files)

# concatenate energy data from each year into single dataframe
joinedData = pd.concat(map(pd.read_csv,joined_list))

# calculate total energy for duplicated rows (i.e. same building number, date, and energy type)
joinedData = joinedData.groupby(['BUILDING_NUMBER', 'START_DATE', 'LEVEL3_CATEGORY']).agg({'MMBTU': 'sum', 'EXT_GROSS_AREA': 'mean'})
joinedData = joinedData.reset_index()
joinedData = joinedData.set_axis(['building', 'date', 'energy_type', 'MMBTU', 'area'], axis=1, inplace=False)

# create column energy per gross area
joinedData['MMBTU_per_area'] = joinedData['MMBTU']/joinedData['area']

# set up for bloom column
joinedData['date'] = pd.to_datetime(joinedData['date'], infer_datetime_format=True) # convert dates to datetime format
joinedData['year'] = pd.DatetimeIndex(joinedData['date']).year # create column with just year extracted

# create new dataframe to calculate max energy for each (energy type, building, year) combination
yearlyMax = joinedData
yearlyMax['year_max_MMBTU'] = yearlyMax['MMBTU']
yearlyMax = yearlyMax.groupby(['building', 'year', 'energy_type']).agg({'year_max_MMBTU': 'max'})
yearlyMax = yearlyMax.reset_index()

# merge max energy for the year into original dataframe
joinedData = joinedData.merge(yearlyMax, how='left', on=['building', 'year', 'energy_type'])

# create column bloom energy as energy/year's max energy (for that energy type and building)
joinedData['MMBTU_bloom'] = joinedData['MMBTU']/joinedData['year_max_MMBTU_y']

# drop unecessary columns
joinedData = joinedData.drop(columns=['area', 'year', 'year_max_MMBTU_x', 'year_max_MMBTU_y'])

# write to file
joinedData.to_csv(filePath + '/dash.csv')


######
# Reorganizing building footprint file
######

building_footprint_filepath = '/building_footprint_coordinates.csv'
buildingFootprintCoordinates = pd.read_csv(filePath + building_footprint_filepath)
buildingFootprints = pd.DataFrame()

for buildingNumber, group in buildingFootprintCoordinates.groupby('BUILDING_NUMBER'):
    polygon = Polygon(zip(group.X, group.Y)) # create a polygon from coordinates
    row = {'building': buildingNumber, 'geometry': polygon}
    buildingFootprints = buildingFootprints.append(row, ignore_index = True) # append row of building number, polygon

# buildingFootprints.to_csv(filePath + '/building-footprint.csv', index=False) # write to file


######
# Combining energy usage and building footprint data
######

data = pd.read_csv(filePath + '/dash.csv')
buildingFootprints = pd.read_csv(filePath + '/building-footprint.csv')

data = data.merge(buildingFootprints, how='left', on='building') # merge building footprint polygons with energy data
data = data.reset_index()
data = data.drop(columns=['Unnamed: 0', 'index'])
print(data.columns)

data.to_csv(filePath + '/dash.csv', index=True)
