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
import numpy as np

<<<<<<< HEAD
filePath = 'C:/Users/einat/D-Lab/net-zero-dlab'
inputSignifier = 'energy_distribution_data_*.csv'
=======
filePath = '/Users/kmak/Desktop/EC.719/Building Energy Visualization/net-zero-dlab/Data files'
inputSignifier = 'input_energy_data-*.csv'
>>>>>>> 8e8d13bbdae2e0265c90150960034ffaeaafaeb6


######
# Reorganizing building energy usage csv files
######


joined_files = os.path.join(filePath, inputSignifier)
joined_list = glob.glob(joined_files)

joinedData = pd.concat(map(pd.read_csv,joined_list))

<<<<<<< HEAD
# culledData = joinedD ata[['START_DATE', 'BUILDING_NUMBER', 'LEVEL3_CATEGORY', 'MMBTU']]
=======
# culledData = joinedData[['START_DATE', 'BUILDING_NUMBER', 'LEVEL3_CATEGORY', 'MMBTU']]
>>>>>>> 8e8d13bbdae2e0265c90150960034ffaeaafaeb6

electricityData = []
steamData = []
chilledWaterData = []

energyDataList = [electricityData, steamData, chilledWaterData]
energyDataTypes = ['Electricity', 'Steam', 'Chilled Water']

for index, data in enumerate(energyDataList):
    data = joinedData[joinedData['LEVEL3_CATEGORY'] == energyDataTypes[index]]
    data['START_DATE'] = pd.to_datetime(data['START_DATE'])
    data = data.sort_values(by = 'START_DATE')
    # data = data.pivot_table(index = 'START_DATE', columns = 'BUILDING_NUMBER', values = 'MMBTU', fill_value='NaN', aggfunc=np.sum)
    data = pd.pivot_table(data, values = 'MMBTU', index = 'START_DATE', columns = 'BUILDING_NUMBER', aggfunc = np.sum) #fill_value = 'NaN'
    data = data.transpose()
    data.to_csv(filePath + '/' + energyDataTypes[index] + '.csv')


######
# Reorganizing building footprint file
######

building_footprint_filepath = '/building_footprint_coordinates.csv'
buildingFootprintCoordinates = pd.read_csv(filePath + building_footprint_filepath)
buildingFootprints = pd.DataFrame()

for buildingNumber, group in buildingFootprintCoordinates.groupby('BUILDING_NUMBER'):
    polygon = Polygon(zip(group.X, group.Y))
    row = {'BUILDING_NUMBER': buildingNumber, 'geometry': polygon}
    buildingFootprints = buildingFootprints.append(row, ignore_index = True)

buildingFootprints.to_csv(filePath + '/building-footprint.csv', index=False)


######
# Combining energy usage and building footprint data
######

electricityData = pd.read_csv(filePath + '/Electricity.csv')
steamData = pd.read_csv(filePath + '/Steam.csv')
chilledWaterData = pd.read_csv(filePath + '/Chilled Water.csv')

buildingFootprints = pd.read_csv(filePath + '/building-footprint.csv')

electricityData = electricityData.merge(buildingFootprints, how='left', on='BUILDING_NUMBER')
steamData = steamData.merge(buildingFootprints, how='left', on='BUILDING_NUMBER')
chilledWaterData = chilledWaterData.merge(buildingFootprints, how='left', on='BUILDING_NUMBER')

electricityData.to_csv(filePath + '/Electricity.csv', index=False)
steamData.to_csv(filePath + '/Steam.csv', index=False)
chilledWaterData.to_csv(filePath + '/Chilled Water.csv', index=False)






