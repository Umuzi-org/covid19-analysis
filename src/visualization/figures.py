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
    'minWidth': '100%',
}
#------------------------Read in data ---------------------------
#SA Cummulative
#---------------- Load datasets -----------
df = pd.read_csv('data/external/global_data.csv')

df2 = pd.read_csv('data/external/SA_from_day1.csv')
df4 = pd.read_csv('data/external/SA_3_daily_update.csv')
df5 = pd.read_csv('data/external/Covid_data.csv')
df6 = pd.read_csv('data/external/covid.csv',delimiter=',')
df3 = pd.read_csv('data/external/Sa_live.csv')
df_day =pd.read_csv('data/external/provincial_cumulative.csv')
# Commulative death per province 
df_death = pd.read_csv('data/external/provincial_death.csv')

df1 = pd.read_csv('data/external/global_data.csv')
df1 = df1[df1.Country=='South Africa']

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
#Summing per column
tot_cases = df.TotalConfirmed.sum()
nw_cases = df.NewConfirmed.sum()
tot_deaths = df.TotalDeaths.sum()
new_deaths = df.NewDeaths.sum()
tot_recover = df.TotalRecovered.sum()
new_recover = df.NewRecovered.sum()
diff = tot_cases - nw_cases
diff2 = tot_recover - new_recover
diff3 = tot_deaths - new_deaths 

#Separating columns

#Corona  cases: Total and New
df_tot_cases = df.loc[:,['Country','TotalConfirmed']].sort_values(by='TotalConfirmed', ascending=False)
df_new_cases = df.loc[:,['Country','NewConfirmed']]

#Death Cases: Total and New 
df_tot_death = df.loc[:,['Country','TotalDeaths']]
df_new_death = df.loc[:,['Country','NewDeaths']]

#Recovery cases: Total and new
df_tot_recover = df.loc[:,['Country','TotalRecovered']]
df_new_recover = df.loc[:,['Country','NewRecovered']]
                      
#Sorting cases by total                     
df_cases = df_tot_cases.merge(df_new_cases, on='Country').sort_values(by=['TotalConfirmed'],
                                                                      ascending=False)
df_death = df_tot_death.merge(df_new_death, on='Country').sort_values(by=['TotalDeaths'],
                                                                      ascending=False)
df_recover = df_tot_recover.merge(df_new_recover, on='Country').sort_values(by=['TotalRecovered'], 
                                                                            ascending=False)
# total cases indicator
fig_ind = go.Figure(go.Indicator(
    
    value = tot_cases,
    delta = {'reference': diff},
    gauge = {
        'axis': {'visible': False}},
    domain = {'row': 0, 'column': 0}))

fig_ind = fig_ind.update_layout(
    template = {'data' : {'indicator': [{
        'title': {'text': "Total Cases"},
        'mode' : "number+delta+gauge",
        }]
                         }})
#Summing per column
tot_cases = df.TotalConfirmed.sum()
nw_cases = df.NewConfirmed.sum()
tot_deaths = df.TotalDeaths.sum()
new_deaths = df.NewDeaths.sum()
tot_recover = df.TotalRecovered.sum()
new_recover = df.NewRecovered.sum()
diff = tot_cases - nw_cases

#Recoveries indicator
fig2 = go.Figure(go.Indicator(
    mode = "number+delta",
    value = tot_recover,
    delta = {'reference': diff2},
    domain = {'row': 0, 'column': 1}))
fig2 = fig2.update_layout(
    template = {'data' : {'indicator': [{
        'title': {'text': "Recoveries"}
        }]
                         }})
# total deaths indicator
fig3 = go.Figure(go.Indicator(
    
    value = tot_deaths,
    delta = {'reference': diff3},
    gauge = {
        'axis': {'visible': False}},
    domain = {'row': 0, 'column': 0}))

fig3 = fig3.update_layout(
    template = {'data' : {'indicator': [{
        'title': {'text': "Total Deaths"},
        'mode' : "number+delta+gauge",
        }]
                         }})
#----- Feature Creation from existing data ----
df['Active Cases'] = df['TotalConfirmed'] - df['TotalRecovered'] - df['TotalDeaths']
df['Closed Cases'] = df['TotalRecovered'] + df['TotalDeaths']
df['Recovery Rate'] = (df['TotalRecovered'] / df['TotalConfirmed'])*100
df['Case Fatality Rate'] = (df['TotalDeaths'] / df['TotalConfirmed']) * 100

#SA commulative data graph
df_rsa = df6[df6.countriesAndTerritories == 'South_Africa'].reset_index()
fig_line = go.Figure()
fig_line.add_trace(go.Scatter(x = df4.timestamp,y= df4.active, name = 'Active Cases in SA'))
fig_line.update_layout(title = 'Commulative confirmed cases in SA as 17/03/2020')

#Total confirmed world map
data = [ dict(
 type='choropleth',
 locations = df['Country'],
 autocolorscale = True,
 z = df['TotalConfirmed'],
 locationmode = 'country names',
 marker = dict(
 line = dict (
 color = 'rgb(255,255,255)',
 width = 2,
 )  ),
 colorbar = dict(
 title = 'Number of cases'
 )
 ) ]
layout = dict(
 autosize=False,
)
fig = go.Figure(data = data, layout = layout)

# Active cases world map

data1 = [ dict(
 type='choropleth',
 locations = df['Country'],
 autocolorscale = True,
 z = df['Active Cases'],
 locationmode = 'country names',
 marker = dict(
 line = dict (
 color = 'rgb(255,255,255)',
 width = 2,
 )  ),
 colorbar = dict(
 title = 'Active cases'
 )
 ) ]
layout = dict(
 autosize=False,   
)
fig1_ = go.Figure(data = data1, layout = layout)

#Closed cases world map
data2 = [ dict(
 type='choropleth',
 locations = df['Country'],
 autocolorscale = True,
 z =df['Closed Cases'],
 locationmode = 'country names',
 marker = dict(
 line = dict (
 color = 'rgb(255, 255, 255)',
 width = 2,
 )  ),
 colorbar = dict(
 title = 'Closed Cases'
 )
 ) ]
layout = dict(
 autosize=False,
    
)
fig2_ = go.Figure(data = data2, layout = layout)

#Recovery Rate World Map

data3 = [ dict(
 type='choropleth',
 locations = df['Country'],
 autocolorscale = True,
 z =df['Recovery Rate'],
 locationmode = 'country names',
 marker = dict(
 line = dict (
 color = 'rgb(255,255,255)',
 width = 2,
 )  ),
 colorbar = dict(
 title = 'Recovery Rate (%)'
 )
 ) ]
layout = dict(
 autosize=False,    
)
fig3_ = go.Figure(data = data3, layout = layout)

#Case fatality rate world map

data4 = [ dict(
 type='choropleth',
 locations = df['Country'],
 autocolorscale = True,
 z =df['Case Fatality Rate'],
 locationmode = 'country names',
 marker = dict(
 line = dict (
 color = 'rgb(255,255,255)',
 width = 2,
 )  ),
 colorbar = dict(
 title = 'Case Fatality Rate (%)'
 )
 ) ]
layout = dict(
    autosize=False,
    
)
fig4_ = go.Figure(data = data4, layout = layout)

fig_prov_stacked = go.Figure(data=[
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
fig_prov_stacked.update_layout(
    updatemenus=[
        dict(
            active=0,
            buttons=list([
                dict(label="ALL",
                     method="update",
                     args=[{"visible": [True,True,True,True,True,True,True,True,True,]},
                           {"title": "Cumulative Confirmed Cases: Eastern Cape",
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
                     args=[{"visible": [False,False,False,True, False,False, False, False]},
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
                          }])
            ]),
        )
    ])
# Change the bar mode
fig_prov_stacked.update_layout(barmode='stack',xaxis=dict(
    rangeslider=dict(
        visible = True)))
fig_prov_stacked.update_layout(title_text="Confirmed Cases by provinces",
                 xaxis_title="Days since the first confirmed case",
                  yaxis_title="Confirmed cases")
                            
#-----------------Provinces commulative log graph-------------------------
# Initialize figure
fig_prov_log = go.Figure()

# Add Traces

fig_prov_log.add_trace(
    go.Scatter(
        y=[2,312],
        x=[2,10],
        line=dict(color='grey',
                  width=4, dash='dot'),
        name = '1st Day'
    ))
fig_prov_log.add_trace(
    go.Scatter(
        y=[2,59],
        x=[3,60],
        line=dict(color='grey',
                  width=4, dash='dot'),
        name = '2nd Day'
    ))
fig_prov_log.add_trace(
    go.Scatter(
        y=[2,36],
        x=[4,60],
        line=dict(color='grey',
                  width=4, dash='dot'),
        name = '3rd Day'
    ))
fig_prov_log.add_annotation(
            x=10,
            y=2.5,
            text="Cases Doubles every day",
)
fig_prov_log.add_annotation(
            x=21,
            y=.8,
            text="Doubles every 2nd day",         
)
fig_prov_log.add_annotation(
            x=40,
            y=1.1,
            text="3rd day",
          
)

fig_prov_log.add_trace(
    go.Scatter(
        y=df_day['EC'],
        x=df_day.index,
        name= 'EC'
    ))
fig_prov_log.add_trace(
    go.Scatter(
        y=df_day['WC'],
        x=df_day.index,
        name= 'WC'
    ))
fig_prov_log.add_trace(
    go.Scatter(
        y=df_day['FS'],
        x=df_day.index,
        name= 'FS'
    ))
fig_prov_log.add_trace(
    go.Scatter(
        y=df_day['GP'],
        x=df_day.index,
        name= 'GP'
    ))
fig_prov_log.add_trace(
    go.Scatter(
        y=df_day['KZN'],
        x=df_day.index,
        name= "KZN"
    ))
fig_prov_log.add_trace(
    go.Scatter(
        y=df_day['NW'],
        x=df_day.index,
        name= 'NW'
    ))
fig_prov_log.add_trace(
    go.Scatter(
        y=df_day['LP'],
        x=df_day.index,
        name= 'LP'
    ))
fig_prov_log.add_trace(
    go.Scatter(
        y=df_day['MP'],
        x=df_day.index,
        name= 'MP'
    ))
fig_prov_log.add_trace(
    go.Scatter(
        y=df_day['NC'],
        x=df_day.index,
        name= 'NC'
    ))
# fig_prov_log.add_trace(
#     go.Scatter(
#         y=df_day['UNKNOWN'],
#         x=df_day.index,
#         name='Unlocated'
#     ))

fig_prov_log.update_layout(
    updatemenus=[
        dict(
            active=0,
            buttons=list([
                dict(label="ALL",
                     method="update",
                     args=[{"visible": [True,True,True,True,True,True,True,True,True,True,True,True,True,]},
                           {"title": "Cumulative Confirmed Cases: Eastern Cape",
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
                     args=[{"visible": [True,True,True,False, False,False,False,False, False,False,False, False,True]},
                           {"title": "Unlocated",
                          }]),
            ]),
        )
    ])
# Set title
fig_prov_log.update_layout(title_text="Confirmed Cases by Province",
                 xaxis_title="Days since the first confirmed case",
                 yaxis_title="Log",
                 yaxis_type="log")
a = df_day.set_index('date')
a = a.diff()
a = a.dropna()
a = a.reset_index()
df_day = a

# Initialize figure
fig_flat = go.Figure()

# Add Traces

fig_flat.add_trace(
    go.Scatter(
        y=[0,800],
        x=[18,18],
        line=dict(color='grey',
                  width=4, dash='dot'),
        name = 'lockdown'
    ))
fig_flat.add_trace(
    go.Scatter(
        y=[0,800],
        x=[55,55],
        line=dict(color='grey',
                  width=4, dash='dot'),
        name = 'level_4'
    ))
fig_flat.add_annotation(
            x=18,
            y=400,
            text="Lockdown starts",
          
)
fig_flat.add_annotation(
            x=55,
            y=500,
            text="Level 4",
          
)
fig_flat.add_trace(
    go.Scatter(
        y=df_day['EC'],
        x=df_day.index,
        name= 'EC'
    ))
fig_flat.add_trace(
    go.Scatter(
        y=df_day['WC'],
        x=df_day.index,
        name= 'WC'
    ))
fig_flat.add_trace(
    go.Scatter(
        y=df_day['FS'],
        x=df_day.index,
        name= 'FS'
    ))
fig_flat.add_trace(
    go.Scatter(
        y=df_day['GP'],
        x=df_day.index,
        name= 'GP'
    ))
fig_flat.add_trace(
    go.Scatter(
        y=df_day['KZN'],
        x=df_day.index,
        name= "KZN"
    ))
fig_flat.add_trace(
    go.Scatter(
        y=df_day['NW'],
        x=df_day.index,
        name= 'NW'
    ))
fig_flat.add_trace(
    go.Scatter(
        y=df_day['LP'],
        x=df_day.index,
        name= 'LP'
    ))
fig_flat.add_trace(
    go.Scatter(
        y=df_day['MP'],
        x=df_day.index,
        name= 'MP'
    ))
fig_flat.add_trace(
    go.Scatter(
        y=df_day['NC'],
        x=df_day.index,
        name= 'NC'
    ))
# fig.add_trace(
#     go.Scatter(
#         y=df_day['UNKNOWN'],
#         x=df_day.index,
#         name='Unlocated'
#     ))



fig_flat.update_layout(
    updatemenus=[
        dict(
            active=0,
            buttons=list([
                dict(label="ALL",
                     method="update",
                     args=[{"visible": [True,True,True,True,True,True,True,True,True,True,True,True,]},
                           {"title": "Cumulative Confirmed Cases: Eastern Cape",
                            }]),
                dict(label="EC",
                     method="update",
                     args=[{"visible": [True,True,True, False, False, False,False, False, False,False, False, False]},
                           {"title": "Cumulative Confirmed Cases: Eastern Cape",
                            }]),
                dict(label="WC",
                     method="update",
                     args=[{"visible": [True,True,False,True,False,False,False,False,False,False,False,False]},
                           {"title": "Cumulative Confirmed Cases: Western Cape",
                          }]),
                dict(label="FS",
                     method="update",
                     args=[{"visible": [True,True,False,False,True,False,False,False,False,False,False,False]},
                           {"title": "Cumulative Confirmed Cases: Free State",
                          }]),
                dict(label="GP",
                     method="update",
                     args=[{"visible": [True,True,False,False,False,True,False,False,False,False,False,False]},
                           {"title": "Cumulative Confirmed Cases: Gauteng",
                          }]),
                dict(label="KZN",
                     method="update",
                     args=[{"visible": [True,True,False,False,False,False,True, False,False,False, False, False]},
                           {"title": "Cumulative Confirmed Cases: Kwa Zulu Natal",
                          }]),
                dict(label="NW",
                     method="update",
                     args=[{"visible": [True,True,False,False,False,False,False,True,False,False, False, False]},
                           {"title": "Cumulative Confirmed Cases: North West",
                          }]),
                dict(label="LP",
                     method="update",
                     args=[{"visible": [True,True,False, False,False,False,False, False,True, False, False, False]},
                           {"title": "Cumulative Confirmed Cases: Limpopo",
                          }]),
                dict(label="MP",
                     method="update",
                     args=[{"visible": [True,True,False, False,False,False,False, False,False,True,  False, False]},
                           {"title": "Cumulative Confirmed Cases: Mpumalanga",
                          }]),
                dict(label="NC",
                     method="update",
                     args=[{"visible": [True,True,False, False,False,False,False, False,False,  False,True, False]},
                           {"title": "Cumulative Confirmed Cases: Northern Cape",
                          }]),
                 dict(label="Cumulative Confirmed Cases: UNKWNOWN",
                     method="update",
                     args=[{"visible": [True,True,False, False,False,False,False, False,False,False, False,True]},
                           {"title": "Unlocated",
                          }]),
            ]),
        )
    ])

# Set title
fig_flat.update_layout(title_text="Is South Africa flattening the curve",
                 xaxis_title="Days since the first confirmed case",
                 yaxis_title="Daily New Cases",
                 )

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
app = dash.Dash(__name__,server=server, 
                external_stylesheets=external_stylesheets,
                url_base_pathname='/cum_province/')

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
def render_content(tab):

    if tab == 'tab-1':
        return html.Div([
            html.Div([

                # VISUALISATIONS

                html.Div([
                      dcc.Graph(
                          id='tot_cases',
                            figure=go.Figure(fig_ind)
                          
                        ),
                html.Div([
                    dash_table.DataTable(
                            id='country_cases',
                            data=df_tot_cases.to_dict("rows"),
                            columns=[{"name": i, "id": i}
                                     for i in df_tot_cases.columns],
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
                            figure=go.Figure(fig2)
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
                            figure=go.Figure(fig3)
                        ),


                    html.Div([
                        dcc.Graph(
                          id='sa_active',
                            figure=go.Figure(fig_line)
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
  

    elif tab == 'tab-2':
        return html.Div([
            
            dcc.Graph(
                id='figure',
                figure=go.Figure(fig_prov_stacked)
            ),html.Div([
                dcc.Graph(
                    id='figure',
                    figure=go.Figure(fig_prov_log)
                ),html.Div([
                dcc.Graph(
                    id='figure',
                    figure=go.Figure(fig_flat)
                ),            
            ], className="row"),
                ], className="twelve columns")])
    else:
        return html.H1('African cases!!!')
    
#---- Small tab call back -----

@app.callback(Output('tabs-globals-contents', 'children'),
              [Input('tabs-globals', 'value')])
def render_content(tabs):
    
    if tabs == 'tab-1.':
        return dcc.Graph(

            id='figure',
            figure=
              go.Figure(fig)
            )
    elif tabs == 'tab-2.':   
        return dcc.Graph(

            id='figure',
            figure=
              go.Figure(fig1_)
            )
           
    elif tabs == 'tab-3.':   
        return dcc.Graph(

            id='figure',
            figure=
              go.Figure(fig2_)
            )
    elif tabs == 'tab-4.':
         return dcc.Graph(
             id='figure',
             figure=go.Figure(fig3_)
            )
    else:
        return dcc.Graph(

            id='figure',
            figure=
              go.Figure(fig4_)
            )


if __name__ == '__main__':
    app.run_server(debug=True)