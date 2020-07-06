import requests
from pandas.io.json import json_normalize
import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from dash.dependencies import Input, Output
from plotly.subplots import make_subplots
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import plotly as py
import plotly.graph_objs as go
init_notebook_mode(connected=True)

#----------- Table styling ------------------
style_cell = {
    'fontFamily': 'Open Sans',
    'textAlign': 'center',
    'height': '30px',
    'padding': '10px 22px',
    'whiteSpace': 'inherit',
    'overflow': 'hidden',
                'textOverflow': 'ellipsis',
}
style_cell_conditional = [
    {
        'if': {'column_id': 'State'},
        'textAlign': 'left'
    },
]
style_header = {
    'fontWeight': 'bold',
    'backgroundColor': "#3D9970",
    'fontSize': '16px'
}
style_data_conditional = [
    {
        'if': {'row_index': 'odd'},
        'backgroundColor': 'rgb(248, 248, 248)'
    }]
style_table = {
    'maxHeight': '70ex',
    'overflowY': 'scroll',
    'width': '100%',
    'minWidth': '100%',}
#Display on dash and flask
import dash
import dash_core_components as dcc
import dash_html_components as html
import flask
#import plotly figures.py as mod 
from visualization import figures as mod

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
server = flask.Flask(__name__)
app = dash.Dash(__name__,server=server, 
                external_stylesheets=external_stylesheets,
                url_base_pathname='/master_covid19-analysis/')


#Style sheet

app.config['suppress_callback_exceptions'] = True
app.layout = html.Div(children=[
        #header
    
    html.Div([
        html.Div([
           
        ], className="four columns"),
        

        html.Div([
            html.H3('Latest Covid 19 Update', style={
                                'fontFamily': 'Open Sans',
                                'textAlign': 'center',
                            }),
             
        ], className="four columns"),
        
        html.Div([
            html.H3('#StayAtHome', style={
                                'fontFamily': 'Open Sans',
                                'textAlign': 'right',
                            }),
            
            
        ], className="four columns")
    ], className="row"),
    
    dcc.Tabs(id='tabs-global', value='tab', children=[
        dcc.Tab(label='Global Map', value='tab-1'),
        dcc.Tab(label='South African cases', value='tab-2'),
        dcc.Tab(label='African cases', value='tab-3'),
    ]),
    html.Div(id='tabs-global-content')
])


#----------- Main tab call back ----
@app.callback(Output('tabs-global-content', 'children'),
              [Input('tabs-global', 'value')])
def render_content(tabs):

    if tabs == 'tab-1':
        return html.Div([
            html.Div([

                # VISUALISATIONS

                html.Div([
                      dcc.Graph(
                          id='tot_cases',
                            figure=go.Figure(mod.fig_ind)
                          
                        ),
                html.Div([
                    dash_table.DataTable(
                            id='country_cases',
                            data=mod.df_tot_cases.to_dict("rows"),
                            columns=[{"name": i, "id": i}
                                     for i in mod.df_tot_cases.columns],
                            style_table=style_table,
                            style_cell=style_cell,
                            style_data_conditional=style_data_conditional,
                            style_header=style_header,
                            style_cell_conditional=style_cell_conditional,
                            filter_action="native"
                        )
                ])          
            ], className="row"),

                ], className="three columns"),
            
            html.Div([
                    dcc.Graph(
                          id='sa_cases',
                            figure=go.Figure(mod.fig2)
                        ),
                    html.Div([
                        dcc.Tabs(id='tabs-globals', value='tabs', children=[
                            dcc.Tab(label='Total Cases', value='tab-1.'),
                            dcc.Tab(label='Active Cases', value='tab-2.'),
                            dcc.Tab(label='Solved Cases', value='tab-3.'),
                            dcc.Tab(label='Recovery Rate', value='tab-4.'),
                            dcc.Tab(label='Case Fatality Rate', value='tab-5.')
                        ], colors={
                                "border": "white",
                                "primary": "gold",
                                "background": "cornsilk"
                            }),
                     html.Div(id='tabs-globals-contents'),
            ], className="row"),
                ], className="six columns"),

                html.Div([
                     dcc.Graph(
                          id='indicator_tot_death',
                            figure=go.Figure(mod.fig3)
                        ),


                    html.Div([
                        dcc.Graph(
                          id='sa_active',
                            figure=go.Figure(mod.fig_line)
                        ),
                            
                       
            ], className="row")

                ], className="three columns"),
            ], className="row")

            # fOOTER
        html.Div([
                html.Div([
                    html.H3('Footer'),

                ], className="six columns"),

                html.Div([
                    html.H3('Footer'),

                ], className="six columns"),
            ], className="row")
  

    elif tabs == 'tab-2':
        return html.Div([
            
            dcc.Graph(
                id='figure',
                figure=go.Figure(mod.fig_prov_stacked)
            ),html.Div([
                dcc.Graph(
                    id='figure',
                    figure=go.Figure(mod.fig_prov_log)
                ),html.Div([
                dcc.Graph(
                    id='figure',
                    figure=go.Figure(mod.fig_flat)
                ),            
            ], className="row"),
                ], className="twelve columns")])
    else:
        return html.Div([
            html.Div([

                # VISUALISATIONS

                html.Div([
                      dcc.Graph(
                          id='total_cases',
                            figure=go.Figure(mod.fig_ind)
                          
                        ),
                html.Div([
                    dash_table.DataTable(
                            id='country_cases',
                            data=mod.df_tot_cases.to_dict("rows"),
                            columns=[{"name": i, "id": i}
                                     for i in mod.df_tot_cases.columns],
                            style_table=style_table,
                            style_cell=style_cell,
                            style_data_conditional=style_data_conditional,
                            style_header=style_header,
                            style_cell_conditional=style_cell_conditional,
                            filter_action="native"
                        )
                ])          
            ], className="row"),

                ], className="three columns"),
            
            html.Div([
                    dcc.Graph(
                          id='africa_cases',
                            figure=go.Figure(mod.fig5)
                        ),
                    html.Div([
                        dcc.Tabs(id='tabs-africa', value='tabs', children=[
                            dcc.Tab(label='Total Cases', value='tab-6.'),
                            dcc.Tab(label='Active Cases', value='tab-7.'),
                            dcc.Tab(label='Solved Cases', value='tab-8.'),
                            dcc.Tab(label='Recovery Rate', value='tab-9.'),
                            dcc.Tab(label='Case Fatality Rate', value='tab-10.')
                        ], colors={
                                "border": "white",
                                "primary": "gold",
                                "background": "cornsilk"
                            }),
                     html.Div(id='tabs-africa-contents'),
            ], className="row"),
                ], className="six columns"),

                html.Div([
                     dcc.Graph(
                          id='indicator_tot_death',
                            figure=go.Figure(mod.fig6)
                        ),


                    html.Div([
                        dcc.Graph(
                          id='africa_active',
                            figure=go.Figure(mod.fig1_line)
                        ),
                            
                       
            ], className="row")

                ], className="three columns"),
            ], className="row")

            # fOOTER
        html.Div([
                html.Div([
                    html.H3('Footer'),

                ], className="six columns"),

                html.Div([
                    html.H3('Footer'),

                ], className="six columns"),
            ], className="row")
  
    
#---- Small tab call back -----

@app.callback(Output('tabs-globals-contents', 'children'),
              [Input('tabs-globals', 'value')])
def render_content(tabs):
    
    if tabs == 'tab-1.':
        return dcc.Graph(
            id='figure',
            figure=
              go.Figure(mod.fig)
            )
    elif tabs == 'tab-2.':   
        return dcc.Graph(

            id='figure',
            figure=
              go.Figure(mod.fig1_)
            )     
    elif tabs == 'tab-3.':   
        return dcc.Graph(
            id='figure',
            figure=
              go.Figure(mod.fig2_)
            )
    elif tabs == 'tab-4.':
         return dcc.Graph(
             id='figure',
             figure=go.Figure(mod.fig3_)
            )
    else:
        return dcc.Graph(
            id='figure',
            figure=
              go.Figure(mod.fig4_)
            )


#---- Small tab call back -----

@app.callback(Output('tabs-global-contents', 'children'),
              [Input('tabs-global', 'value')])
def render_content(tabs):
    
    if tabs == 'tab-5.':
        return dcc.Graph(
            id='figure',
            figure=
              go.Figure(mod.fig4_)
            )
    elif tabs == 'tab-6.':   
        return dcc.Graph(

            id='figure',
            figure=
              go.Figure(mod.fig5_)
            )     
    elif tabs == 'tab-7.':   
        return dcc.Graph(
            id='figure',
            figure=
              go.Figure(mod.fig6_)
            )
    elif tabs == 'tab-8.':
         return dcc.Graph(
             id='figure',
             figure=go.Figure(mod.fig7_)
            )
    else:
        return dcc.Graph(
            id='figure',
            figure=
              go.Figure(mod.fig8_)
            )
    
if __name__ == '__main__':
    app.run_server(debug=True)
    
        
        
     
    

