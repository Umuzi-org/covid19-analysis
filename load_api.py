import requests
from pandas.io.json import json_normalize
import pandas as pd

#--------Global cases and data from JH uni ----
url = 'https://api.covid19api.com/summary'
r = requests.get(url)
dictr = r.json()
header = dictr['Countries']
df = pd.json_normalize(header)

#---- Confirmed cases in South Africa in the last 20 days---->
url1 = 'https://api.covid19api.com/live/country/south-africa/status/confirmed/date/2020-03-21T13:13:30Z'
df1 = pd.read_json(url1, orient='columns')

#----South African cases from day one ----
url2 = 'https://api.covid19api.com/country/south-africa/status/confirmed'
df2 = pd.read_json(url2, orient='columns')

#---------- SA live ---------
url3 = 'https://api.covid19api.com/country/south-africa/status/confirmed/live'
df3 = pd.read_json(url3, orient='columns')

url4 = 'https://covid19.soficoop.com/country/za'
url5 = 'https://api.covid19api.com/total/dayone/country/south-africa'
df5 = pd.read_json(url5, orient='columns')

#Daily Commulative dataframe 
df4 = requests.get(url4).json()
df4= pd.json_normalize(df4,record_path ='snapshots')


#---------Provincial cumulative timeline confirmed ---------------------
df_day = pd.read_csv('https://raw.githubusercontent.com/dsfsi/covid19za/master/data/covid19za_provincial_cumulative_timeline_confirmed.csv')

#------Provincial Cummulative death -----

df_pr_death = pd.read_csv('https://raw.githubusercontent.com/dsfsi/covid19za/master/data/covid19za_provincial_cumulative_timeline_deaths.csv')

#----- Provincial testing timeline ----
df_testing = pd.read_csv('https://raw.githubusercontent.com/dsfsi/covid19za/master/data/covid19za_provincial_cumulative_timeline_testing.csv',error_bad_lines=False)

#--------- API to CSV -----



df.to_csv('data/external/global_data.csv')
df1.to_csv('data/external/SA_last20days.csv')
df2.to_csv('data/external/SA_from_day1.csv')
df3.to_csv('data/external/Sa_live.csv')
df4.to_csv('data/external/SA_hourly_update.csv')
df5.to_csv('data/external/Covid_data.csv')
df_day.to_csv('data/external/provincial_cumulative.csv')
df_pr_death.to_csv('data/external/provincial_death.csv')
df_testing.to_csv('data/external/provincial_testing.csv')
