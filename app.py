#Imports
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, ALL, State

df = pd.read_csv('meteorites_new')
print(df.info())
df = df.drop('Unnamed: 0', axis=1)

fig = go.Figure(
    data=go.Scattergeo(
        lon = df['reclong'],
        lat = df['reclat'],
        text = df['text'],
        mode = 'markers',
        marker = dict(
            size = 8,
            opacity = 0.8,
            reversescale = True,
            autocolorscale = False,
            symbol = 'circle',
            line = dict(
                width=1,
                color='rgba(102, 102, 102)'
            ),
            colorscale = 'Viridis',
            cmin = 0,
            color = df['mass (kg)'],
            cmax = df['mass (kg)'].max(),
            colorbar_title="Mass of meteorite (in kg)"
        )
    )
)

fig.update_layout(
        title = 'Meteorite landings',
        height = 600, 
        geo = dict(
            showland = True,
            landcolor = "rgb(100, 100, 100)",
            subunitcolor = "rgb(0, 0, 0)",
            countrycolor = "rgb(0, 0, 0)",
            countrywidth = 1,
            subunitwidth = 1
        )
    )

app = dash.Dash(__name__)
server = app.server
app.layout = html.Div(
    children=[html.Div(
            style={
                'backgroundColor':'#303030',
                'color':'white',
                'fontFamily': '"Lucida Console", "Courier New"'
            },
            children=[
                html.H1(
                    style = {
                        'textAlign': 'center',
                    },
                    children="Meteorites fallen on earth",
                    className="header-title" 
                ), #Header title
                html.H2(
                    style = {
                        'textAlign': 'center',
                    },
                    children="A dashboard to visualize one of humanity's biggest existential threats",
                    className="header-description", 
                ),
            ],
            className="header",
    ),#Description below the header        
        html.Div(
            children=[
                html.Div(children = 'Year', 
                        style={'paddingTop':'5px',
                                'fontSize': "20px",
                                'fontFamily': '"Lucida Console", "Courier New"'
                                },
                        className = 'menu-title'),
                dcc.Dropdown(
                    id = 'year-filter',
                    options = [
                        {'label': Year, 'value': Year}
                       for Year in np.append(np.sort(df.year.unique()),"All")
                    ], #'Year' is the filter
                    value = "All",
                    className = 'dropdown', style={'fontSize': "20px",
                                                    'textAlign': 'center',
                                                    'fontFamily': '"Lucida Console", "Courier New", monospace'},
                ),
            ],
            className = 'menu',
),
    html.Div(
            children=[
                html.Div(children = 'Would you want to see the most significant meteorites in history (top 0.1% in terms of mass in kg) ?', 
                style={'paddingTop':'15px',
                        'fontSize': "20px",
                        'fontFamily': '"Lucida Console", "Courier New"'},
                className = 'menu-title'),
                dcc.Checklist(
                    ['Yes'],
                    id = "checklist",
                    inline=True,
                    value = "",
                    style={'paddingTop':'5px',
                        'fontSize': "20px",
                        'fontFamily': '"Lucida Console", "Courier New"'}
                    ),
                ],
            className = 'menu'),

#Adding the world visual
html.Div(
            children=[
                html.Div(
                children = dcc.Graph(
                    id = 'world_chart',
                    figure = fig,
                ),
                style={'width': '100%', 'display': 'inline-block'},
            )])
]) #the dropdown function

#Callback to create interaction
@app.callback(
    dash.dependencies.Output("world_chart", "figure"), 
    [dash.dependencies.Input("year-filter", "value"),
    dash.dependencies.Input("checklist", "value")],
)

def update_charts(Year, val):
    if val == ["Yes"] and Year == "All": 
        filtered_data = df[df['top 0.1% mass']==True]
    else:
        if Year == "All": 
            filtered_data = df
        else:
            Year = int(Year)
            filtered_data = df[df["year"] == Year]
    
    fig = go.Figure(data=go.Scattergeo(
        lon = filtered_data['reclong'],
        lat = filtered_data['reclat'],
        text = filtered_data['text'],
        mode = 'markers',
        marker = dict(
            size = 8,
            opacity = 0.8,
            reversescale = True,
            autocolorscale = False,
            symbol = 'circle',
            line = dict(
                width=1,
                color='rgba(102, 102, 102)'
            ),
            colorscale = 'Viridis',
            cmin = 0,
            color = filtered_data['mass (kg)'],
            cmax = filtered_data['mass (kg)'].max(),
            colorbar_title="Mass of meteorite (in kg)"
        )
    )
)
    return fig

fig.update_layout(
        title = 'Meteorite landings',
        height = 600,
        geo = dict(
            showland = True,
            landcolor = "rgb(100, 100, 100)",
            subunitcolor = "rgb(0, 0, 0)",
            countrycolor = "rgb(0, 0, 0)",
            countrywidth = 0.5,
            subunitwidth = 0.5
        ),
    )

#Running dashboard
if __name__ == '__main__':
    app.run_server()
