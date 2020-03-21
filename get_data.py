import pandas as pd
import requests
import io

URL_confirmed = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv"
s_confirmed = requests.get(URL_confirmed).content
raw_data_confirmed = pd.read_csv(io.StringIO(s_confirmed.decode('utf-8')))
raw_data_confirmed.to_csv('covid19_temp/raw_data_confirmed_latest.csv', index=False)

URL_deaths = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Deaths.csv"
s_deaths = requests.get(URL_deaths).content
raw_data_deaths = pd.read_csv(io.StringIO(s_deaths.decode('utf-8')))
raw_data_deaths.to_csv('covid19_temp/raw_data_deaths_latest.csv', index=False)