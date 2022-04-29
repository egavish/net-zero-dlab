#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 18:22:47 2022

@author: kmak
"""

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

filePath = '/Users/kmak/Desktop/EC.719/Building Energy Visualization/net-zero-dlab/Data files' ##change to your filename
inputSignifier = 'input_energy_data-*.csv'


######
# Reorganizing building energy usage csv files
######


joined_files = os.path.join(filePath, inputSignifier)
joined_list = glob.glob(joined_files)

data = pd.concat(map(pd.read_csv,joined_list))

data['MMBTU_per_area'] = data['MMBTU']/data['EXT_GROSS_AREA']
data = pd.pivot_table(data, values = 'MMBTU_per_area', index = ['START_DATE', 'LEVEL3_CATEGORY'], columns = 'BUILDING_NUMBER', aggfunc = np.sum)
data = data.reset_index()
data = data.rename(columns={"START_DATE": "date", "LEVEL3_CATEGORY": "energy_type"}, errors='raise')

data.to_csv(filePath + '/clustering.csv', index=False)        




