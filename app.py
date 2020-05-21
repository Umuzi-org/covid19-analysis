import flask
from flask import Flask, render_template
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly as py
import plotly.graph_objects as go

#------------------------Read in data ---------------------------
#SA Cummulative
df1 = pd.read_csv('data/external/global_data.csv')
df1 = df1[df1.Country=='South Africa']
df = pd.read_csv('data/external/SA_hourly_update.csv')

#Provincial cummulative
df_day=pd.read_csv('data/external/provincial_cumulative.csv')

# Commulative death per province 

df_death = pd.read_csv('data/external/provincial_death.csv')

#Drop unwanted columns
# Provincial cases dataset
df_day = df_day.drop(['source','Unnamed: 0','YYYYMMDD'],axis = 1)

#append dates with missing data with previous day data(bc commulative)
df_day = df_day.fillna(method='ffill')

df_death = df_death.drop(['source','Unnamed: 0','YYYYMMDD'],axis = 1)
#append dates with missing data with previous day data(bc commulative)
df_death = df_death.fillna(method='ffill')

#Update for the most recent  hours: SA Cases
# df.tail()



fig0 = go.Figure(data=[
    go.Bar( name='GP',x=df_day.index, y=df_day.GP),
    go.Bar( name='WC',x=df_day.index, y=df_day.WC),
    go.Bar( name='KZN',x=df_day.index, y=df_day.KZN),
    go.Bar( name='EC',x=df_day.index, y=df_day.EC),
    go.Bar( name='NW',x=df_day.index, y=df_day.NW),
    go.Bar( name='NC',x=df_day.index, y=df_day.NC),
    go.Bar( name='MP',x=df_day.index, y=df_day.MP),
    go.Bar( name='LP',x=df_day.index, y=df_day.LP),
    go.Bar( name='FS',x=df_day.index, y=df_day.FS),
])
fig0.update_layout(
    updatemenus=[
        dict(
            active=0,
            buttons=list([
                dict(label="ALL",
                     method="update",
                     args=[{"visible": [True,True,True,True,True,True,True,True,True,]},
                           {"title": "Cumulative Confirmed Cases of all Provinces",
                            }]),
                dict(label="GP",
                     method="update",
                     args=[{"visible":  [True, False, False,False, False, False,False, False, False]},
                           {"title": "Cumulative Confirmed Cases: Gauteng",
                            }]),
                dict(label="WC",
                     method="update",
                     args=[{"visible": [False,True,False,False,False,False,False,False,False]},
                           {"title": "Cumulative Confirmed Cases: Western Cape",
                          }]),
                dict(label="KZN",
                     method="update",
                     args=[{"visible": [False,False,True,False,False,False,False,False,False]},
                           {"title": "Cumulative Confirmed Cases: Kwa-Zulu Natal",
                          }]),
                dict(label="EC",
                     method="update",
                     args=[{"visible": [False,False,False,True,False,False,False,False,False]},
                           {"title": "Cumulative Confirmed Cases: Eastern Cape",
                          }]),
                dict(label="NW",
                     method="update",
                     args=[{"visible": [False,False,False,False,True, False,False, False, False]},
                           {"title": "Cumulative Confirmed Cases: North West",
                          }]),
                dict(label="NC",
                     method="update",
                     args=[{"visible": [False,False,False,False,False,True,False, False, False]},
                           {"title": "Cumulative Confirmed Cases: Northern Cape",
                          }]),
                dict(label="MP",
                     method="update",
                     args=[{"visible": [ False,False,False,False, False,False, True, False, False]},
                           {"title": "Cumulative Confirmed Cases: Mpumalanga",
                          }]),
                dict(label="LP",
                     method="update",
                     args=[{"visible": [ False,False,False,False, False,False,False,True,   False]},
                           {"title": "Cumulative Confirmed Cases: Limpopo",
                          }]),
                 dict(label="FS",
                     method="update",
                     args=[{"visible": [ False,False,False,False, False,False,False, False,True]},
                           {"title": "Cumulative Confirmed Cases: Free State",
                          }]),
            ]),
        )
    ])
# Change the bar mode
fig0.update_layout(barmode='stack',xaxis=dict(
    rangeslider=dict(
        visible = True)))
fig0.update_layout(height=600, width=800, title_text="Confirmed Cases by provinces",
                 xaxis_title="Days since the first confirmed case",
                  yaxis_title="Linear")
                            

# Initialize figure
fig1 = go.Figure()

# Add Traces

fig1.add_trace(
    go.Scatter(
        y=[2,312],
        x=[2,10],
        line=dict(color='grey',
                  width=4, dash='dot'),
        name = '1st Day'
     
    ))
fig1.add_trace(
    go.Scatter(
        y=[2,59],
        x=[3,60],
        line=dict(color='grey',
                  width=4, dash='dot'),
        name = '2nd Day'
     
    ))
fig1.add_trace(
    go.Scatter(
        y=[2,36],
        x=[4,60],
        line=dict(color='grey',
                  width=4, dash='dot'),
        name = '3rd Day'
     
    ))


fig1.add_annotation(
            x=10,
            y=2.5,
            text="Cases Doubles every day",
          
)
fig1.add_annotation(
            x=21,
            y=.8,
            text="Doubles every 2nd day",
          
)

fig1.add_annotation(
            x=40,
            y=1.1,
            text="3rd day",
          
)


fig1.add_trace(
    go.Scatter(
        y=df_day['EC'],
        x=df_day.index,
        name= 'EC'
    ))
fig1.add_trace(
    go.Scatter(
        y=df_day['WC'],
        x=df_day.index,
        name= 'WC'
    ))
fig1.add_trace(
    go.Scatter(
        y=df_day['FS'],
        x=df_day.index,
        name= 'FS'
    ))
fig1.add_trace(
    go.Scatter(
        y=df_day['GP'],
        x=df_day.index,
        name= 'GP'
    ))
fig1.add_trace(
    go.Scatter(
        y=df_day['KZN'],
        x=df_day.index,
        name= "KZN"
    ))
fig1.add_trace(
    go.Scatter(
        y=df_day['NW'],
        x=df_day.index,
        name= 'NW'
    ))
fig1.add_trace(
    go.Scatter(
        y=df_day['LP'],
        x=df_day.index,
        name= 'LP'
    ))
fig1.add_trace(
    go.Scatter(
        y=df_day['MP'],
        x=df_day.index,
        name= 'MP'
    ))
fig1.add_trace(
    go.Scatter(
        y=df_day['NC'],
        x=df_day.index,
        name= 'NC'
    ))
# fig1.add_trace(
#     go.Scatter(
#         y=df_day['UNKNOWN'],
#         x=df_day.index,
#         name='Unlocated'
#     ))



fig1.update_layout(
    updatemenus=[
        dict(
            active=0,
            buttons=list([
                dict(label="ALL",
                     method="update",
                     args=[{"visible": [True,True,True,True,True,True,True,True,True,True,True,True,False,]},
                           {"title": "Cumulative Confirmed Cases of all Provinces",
                            }]),
                dict(label="EC",
                     method="update",
                     args=[{"visible": [True,True,True,True, False, False, False,False, False, False,False, False, False]},
                           {"title": "Cumulative Confirmed Cases: Eastern Cape",
                            }]),
                dict(label="WC",
                     method="update",
                     args=[{"visible": [True,True,True,False,True,False,False,False,False,False,False,False,False]},
                           {"title": "Cumulative Confirmed Cases: Western Cape",
                          }]),
                dict(label="FS",
                     method="update",
                     args=[{"visible": [True,True,True,False,False,True,False,False,False,False,False,False,False]},
                           {"title": "Cumulative Confirmed Cases: Free State",
                          }]),
                dict(label="GP",
                     method="update",
                     args=[{"visible": [True,True,True,False,False,False,True,False,False,False,False,False,False]},
                           {"title": "Cumulative Confirmed Cases: Gauteng",
                          }]),
                dict(label="KZN",
                     method="update",
                     args=[{"visible": [True,True,True,False,False,False,False,True, False,False,False, False, False]},
                           {"title": "Cumulative Confirmed Cases: Kwa Zulu Natal",
                          }]),
                dict(label="NW",
                     method="update",
                     args=[{"visible": [True,True,True,False,False,False,False,False,True,False,False, False, False]},
                           {"title": "Cumulative Confirmed Cases: North West",
                          }]),
                dict(label="LP",
                     method="update",
                     args=[{"visible": [True,True,True,False, False,False,False,False, False,True, False, False, False]},
                           {"title": "Cumulative Confirmed Cases: Limpopo",
                          }]),
                dict(label="MP",
                     method="update",
                     args=[{"visible": [True,True,True,False, False,False,False,False, False,False,True,  False, False]},
                           {"title": "Cumulative Confirmed Cases: Mpumalanga",
                          }]),
                dict(label="NC",
                     method="update",
                     args=[{"visible": [True,True,True,False, False,False,False,False, False,False,  False,True, False]},
                           {"title": "Cumulative Confirmed Cases: Northern Cape",
                          }]),
                 dict(label="Cumulative Confirmed Cases: UNKWNOWN",
                     method="update",
                     args=[{"visible": [True,True,True,False, False,False,False,False, False,False,False, False,False]},
                           {"title": "Unlocated",
                          }]),
            ]),
        )
    ])

# Set title
fig1.update_layout(title_text="Confirmed Cases by Province",
                 xaxis_title="Days since the first confirmed case",
                 yaxis_title="Log",
                 yaxis_type="log")

#Display on dash and flask
import dash
import dash_core_components as dcc
import dash_html_components as html
import flask

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
server = flask.Flask(__name__)
App = dash.Dash(__name__,server=server, 
                external_stylesheets=external_stylesheets,
                url_base_pathname='/cum_province/')


App.layout = html.Div(children=[
    
    html.Div(children='Comulative data by province.'
    ),

    dcc.Graph(
        id='linear_bar',
        figure=fig0
    ),
    dcc.Graph(
        id='log_commulative',
        figure=fig1
    )
])

# app = Flask(__name__)

# @app.route('/')

# def index():
#     return render_template('index.html')

if __name__ == '__main__':
    App.run_server(debug=True)