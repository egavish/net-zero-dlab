#!/usr/bin/env python
# coding: utf-8

# # MIT Building Energy Usage

# The goal of this project is to visualize MIT building energy usage over the past ten years. This is part of a broader project to understand MIT's building energy consumption, investigate trends, patterns, and inefficiencies, and ultimately, find a way to get to net zero energy emissions potentially through the use of advanced thermal heat pumps.
# 
# This notebook demonstrates the process behind creating an interactive choropleth map of MIT's building energy usage from preliminary data collection to the end. The graphic will contain the following features:
# - map of MIT campus
# - building's colored according to energy consumption
# - timeslider with montly divisions spanning 10 years
# - menu to select between buildings' chilled water, electricity, and steam usage
# - toggle to view energy consumption on an absolute scale, as energy/gross area, or energy/yearly max (in other words, the seasonal blooming behavior)
# 
# Below is a static image of the final result to give context while reading through the notebook. 

# ![title](img/final-result.png)

# # Imports

# In[1]:


# data imports
import pandas as pd
import geopandas as gpd

#plotly imports
import plotly.graph_objects as go

#generic imports
import numpy as np
from dateutil.relativedelta import relativedelta

# dash imports
from dash import dcc, html, Dash
from dash.dependencies import Input, Output, State


# # Data Manipulation

# In this section we read from input csv files into a pandas dataframe, remove eroneous data, and manipulate the data to be in a convienient format for processing in the plot.

# In[2]:


# read csv file
url = 'https://raw.githubusercontent.com/egavish/net-zero-dlab/main/Data%20files/dash.csv'
energy = pd.read_csv(url)


# In[3]:


# remove buildings without a geometry
energy = energy.dropna(subset=['geometry'], axis=0, inplace=False)


# In[4]:


# remove all rows for energy types not Chilled Water, Electricity, or Steam
# there are a few rows for Gas, etc. that are irrelevant here because there is so little data
energy = energy[ (energy['energy_type'] == 'Chilled Water') | 
                (energy['energy_type'] == 'Electricity') | 
               (energy['energy_type'] == 'Steam')]


# In[5]:


# remove data for building W97 because the raw building footprint for W97 is incorrect
energy = energy[energy.building != 'W97']


# In[6]:


# convert type of date column from string to datetime
energy['date'] = pd.to_datetime(energy['date'], infer_datetime_format=True)


# In[7]:


# define a function to convert a time into months since the initial data measurement
# to be used for time interpretation with a time slider later
startDate = energy['date'].min() # earliest measurement date
def monthsSince(date):
    diff = relativedelta(pd.to_datetime(date), pd.to_datetime(startDate)) # find time difference from initial measurement date
    return diff.months + diff.years * 12 # convert to months


# In[8]:


# create a new column storing the months since version of the date
energy['months_since'] = energy['date'].apply(monthsSince)


# # Building Footprint

# Here we create a geojson file that maps each building number to a list of coordinates representing the building outline. When creating the map, this allows us to correctly link between the building foorprint and the energy value via the building number.

# In[9]:


# function to convert dataframe to geojson
def df_to_geojson(df, properties, geometry='geometry'):
    # create a new python dict to contain our geojson data, using geojson format
    geojson = {'type':'FeatureCollection', 'features':[]}

    # loop through each row in the dataframe and convert each row to geojson format
    for _, row in df.iterrows():
        # create a feature template to fill in
        feature = {'type':'Feature',
                   'properties':{},
                   'geometry':{'type':'Polygon',
                               'coordinates':[]}}

        polygon = row['geometry']
        feature['geometry']['coordinates'] = [np.asarray(polygon.exterior.coords).tolist()]

        # for each column, get the value and add it as a new feature property
        for prop in properties:
            feature['properties'][prop] = row[prop]
        
        # add this feature (aka, converted dataframe row) to the list of features inside our dict
        geojson['features'].append(feature)
    
    return geojson


# In[10]:


# read in building footprint data
url = 'https://raw.githubusercontent.com/egavish/net-zero-dlab/main/Data%20files/building-footprint.csv'
buildingFootprints = pd.read_csv(url)
# convert values in geometry column from strings to Geometry objects
buildingFootprints['geometry'] = gpd.GeoSeries.from_wkt(buildingFootprints['geometry'])

# call previously defined function to create geojson
properties=['building']
geojson = df_to_geojson(buildingFootprints, properties)


# # Helper Functions for Map Display

# This defines several functions to be used for the stylistic layout and design of the map.

# In[11]:


# convert a date to a convenient string representation
# for example, turns 2010-02-01 00:00:00 into 02/10
def dateMark(date):
    return str(date)[5:7] + '/' + str(date)[2:4]

# finds date m months from first measurement date
def dateFrom(m):
    return relativedelta(months = m) + pd.to_datetime(startDate)


# In[12]:


# only show every slider labels every 4 months
def markDisplay(i):
    if i % 4 == 0:
        return 'block'
    return 'none'

# show every 12th month on the time slider in blue
def colorDisplay(i):
    if i % 12 == 0:
        return 'blue'


# In[13]:


# colorbar label depending on energy format
def colorbarLabel(energyFormat):
    if energyFormat == 'MMBTU':
        return 'MMBTU'
    if energyFormat == 'MMBTU_per_area':
        return 'MMBTU/area'
    if energyFormat == 'MMBTU_bloom':
        return '% bloom'


# In[14]:


# sets the max colorbar value depending on which plot is being displayed
def zmax(energyType, energyFormat):
    if energyFormat == 'MMBTU_per_area':
        return 0.02
    if energyFormat == 'MMBTU_bloom':
        return 1
    if energyType == 'Chilled Water':
        return 6000
    if energyType == 'Electricity':
        return 6000
    if energyType == 'Steam':
        return 12000


# # Interactive Choropleth Map

# We use the [Dash](https://dash.plotly.com/introduction) framework to create an interactive choropleth map of MIT building energy usage over time as explained at the beginning. Dash is a written on top of Plotly.js (a charting library) and React.js (a library for building user interfaces) and encorporates html (language for web page content and styling) and css (styling language) for styling and non-chart content.
# 
# In general the framework for creating a dash app is to define the layout of the app including all static content, interactive content, and placeholders for the outputs from user interaction. This is mainly in html and css. As you will see, we will make use of several pre-build app elements like drop down menus, radio buttons, and sliders.
# 
# The `id` tags in the layout section below connects the layout elements to the `Inputs` and `Outputs` of a later function which describes the user interaction.

# In[15]:


app = Dash(__name__) # creates app framework
server = app.server

# describes the layout of the app, uses an html/css framework
app.layout = html.Div([
    # menu selector items
    html.Div([
        html.Div([
            html.H3('Energy Type'), # menu title
            # dropdown menu for each of the different energy types Chilled Water, Electricity, and Steam
            dcc.Dropdown(
                energy['energy_type'].unique(),
                'Chilled Water', # default value
                id='energy-type'
            ),
        ], style={'width': '48%', 'display': 'inline-block'}), # display formating
        
        html.Div([
            html.H3('Data Format'), # menu title
            # buttons for each of the energy formats: absolute, per area, and yearly bloom
            dcc.RadioItems(
                options=[
                    {'label':'Absolute', 'value':'MMBTU'},
                    {'label':'Per Area', 'value':'MMBTU_per_area'},
                    {'label':'Yearly Bloom', 'value':'MMBTU_bloom'}
                ],
                value='MMBTU', # default value
                id='energy-format',
                inline=True,
                inputStyle={'margin-left': '20px',
                           'margin-right': '5px'}
            )
        ], style={'width': '48%', 
                  'float': 'right', 
                  'display': 'inline-block', 
                  'padding': '5px 0px 5px 0px'},
        ) # display formating
        
    ]),

    # placeholder for graph to be created below
    dcc.Graph(id='choropleth-mapbox'),

    # placeholder for month label
    html.H4(
        id='date-output',
        style={'text-align': 'center',
              'font-size': '15px'}
    ),
    
    # time slider 
    dcc.Slider(
        monthsSince(energy['date'].min()), # start value
        monthsSince(energy['date'].max()), # end value
        step=None,
        id='date--slider',
        value=monthsSince(energy['date'].min()), # default value
        marks={ # mark formatting and labeling
            monthsSince(date): {'label': dateMark(date), 
                                'style': 
                                    {'display': markDisplay(i),
                                     'transform': 'rotate(-45deg)',
                                    'color': colorDisplay(i)}} 
            for i, date in enumerate(energy['date'].unique())
        },
        updatemode='drag'
    )
])


# Next are one or more `@app.callback` functions which specify how the app should react to user input.
# 
# In this section, first defined are the `Outputs` and `Inputs`. `Inputs` are all user interactions that should result in a rerendering of the app and `Outputs` are all app elements that should be updated in response to a change in `Input`. In other words, every time an `Input` is changed, the update function gets called, and the `Outputs` are updated. Inputs and Outputs are written as `Input('id name', 'layout property to be changed')`.
# 
# In the function, we select the section of the dataframe we would like to display based on the input values, and create a choropleth map from this subsection.
# 
# The function returns values separated by commas cooresponding to the `Outputs` listed (in order).

# In[16]:


@app.callback(
    Output('choropleth-mapbox', 'figure'), # Output: graph
    Output('date-output', 'children'), # Output: graph
    Input('energy-type', 'value'), # Input: dropdown menu energy type (chilled water, etc.)
    Input('energy-format', 'value'), # Input: radio button energy format (absolute, etc.)
    Input('date--slider', 'value')) # Input: time slider
def update_graph(energy_type_name, energy_format_name, date_value):
    datedf = energy[energy['months_since'] == date_value] # extract rows for particular month according to slider
    dff = datedf[datedf['energy_type'] == energy_type_name] # extract rows of particular energy type according to dropdown
    
    fig = go.Figure() # figure holder
    # creates Choropleth map
    fig.add_trace(
            go.Choroplethmapbox(
                geojson=geojson, # describes geometries
                featureidkey = 'properties.building', # building number as id linking geometries to energy data
                locations = dff.building, # building number as id linking geometries to energy data
                z = dff[energy_format_name], # color mapped from values in MMBTU or MMBTU_per_area etc. column
                
                # colorbar stylistic parameters
                colorscale='Reds',
                zmin = 0,
                zmax = zmax(energy_type_name, energy_format_name),
                showscale=True,
                colorbar={'title': colorbarLabel(energy_format_name)},
         )
    )
    
    # describes container layout for map
    fig.update_layout(
          title=f'{energy_type_name} Usage',
          mapbox_style='carto-positron',
          autosize=True,
          mapbox_center={'lat':42.359, 'lon':-71.095},
          mapbox_zoom=14
        
    )

    fig.update_layout(margin={'l': 0, 'b': 0, 't': 70, 'r': 0}, hovermode='closest')

    return fig, f'{dateMark(dateFrom(date_value))}'


# In[17]:


# runs app
if __name__ == '__main__':
    app.run_server(debug=True)

