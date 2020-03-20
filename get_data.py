import pandas as pd
import requests
import io

URL = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv"
s = requests.get(URL).content
raw_data = pd.read_csv(io.StringIO(s.decode('utf-8')))
raw_data.to_csv('covid19_temp/raw_data_latest.csv', index=False)