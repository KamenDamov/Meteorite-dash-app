#Imports
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt 
import plotly.express as px
#%matplotlib inline
import functools as f
import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

df = pd.read_csv('Meteorite_Landings.csv')
df = df.dropna()

app = dash.Dash(__name__)
app.layout = html.Div(
    children=[html.Div(
            children=[
                html.H1(
                    children="meteorites",style={'textAlign': 'center'}, className="header-title" 
                ), #Header title
                html.H2(
                    children="Meteorites fallen on earth",
                    className="header-description", style={'textAlign': 'center'},
                ),
            ],
            className="header",style={'backgroundColor':'#F5F5F5'},
    ),#Description below the header
        
        
        html.Div(
            children=[
                html.Div(children = 'Year', style={'fontSize': "24px"},className = 'menu-title'),
                dcc.Dropdown(
                    id = 'year-filter',
                    options = [
                        {'label': Year, 'value':Year}
                       for Year in np.sort(df.year.unique())
                    ], #'Year' is the filter
                    value ='2010',
                    clearable = False,
                    searchable = False,
                    className = 'dropdown', style={'fontSize': "24px",'textAlign': 'center'},
                ),
            ],
            className = 'menu',
),
html.Div(
            children=[
                html.Div(children = 'Fall', style={'fontSize': "24px"},className = 'menu-title'),
                dcc.Dropdown(
                    id = 'fell-found-filter',
                    options = [
                        {'label': fall, 'value':fall}
                       for fall in np.sort(df.fall.unique())
                    ], #'Year' is the filter
                    value ='2010',
                    clearable = False,
                    searchable = False,
                    className = 'dropdown', style={'fontSize': "24px",'textAlign': 'center'},
                ),
            ],
            className = 'menu')
]) #the dropdown function

#Running dashboard
if __name__ == '__main__':
    app.run_server()