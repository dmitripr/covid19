import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import DateTime
from datetime import timedelta
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

country = 'Brazil'

raw_data = pd.read_csv('covid19_temp/raw_data_latest.csv')
cols = list(raw_data)
cols[1], cols[0] = cols[0], cols[1]
raw_data = raw_data.loc[:, cols]

raw_data_daily = raw_data.iloc[:, 0:4].join(raw_data.iloc[:, 4:].subtract(raw_data.iloc[:, 4:].shift(axis=1), axis=1))
raw_data.loc['World Total'] = raw_data.sum(numeric_only=True, axis=0)

raw_data_daily = raw_data_daily.set_index('Country/Region')
raw_data_daily.drop(labels=['Lat', 'Long', '1/22/20'], axis=1, inplace=True)
raw_data_daily.loc['World Total'] = raw_data_daily.sum(numeric_only=True, axis=0)

# calculating country data

country_data = raw_data_daily.loc[[country]].groupby(level=0).sum().transpose()
country_data.index = pd.to_datetime(country_data.index)
country_data['T-1'] = country_data[country].shift(periods=1, axis=0)
country_data['prc_daily_increase'] = (country_data[country] / country_data['T-1']) - 1
country_data.drop(columns='T-1', inplace=True)

for i in [3, 4, 5, 6, 7, 8]:
    country_data['T-'+str(i)] = country_data[country].shift(periods=i, axis=0)
    country_data['R0_T-'+str(i)] = country_data[country] / country_data['T-'+str(i)]

country_data.replace([np.inf, -np.inf], np.nan, inplace=True)

for i in [3, 4, 5, 6, 7, 8]:
    print("R0 T-"+str(i)+": {}".format(country_data['R0_T-'+str(i)].mean()))

for i in [3, 4, 5, 6, 7, 8]:
    country_data['pred_T-'+str(i)] = country_data[country]

date_index = pd.date_range(min(country_data.index),max(country_data.index)+timedelta(days=30),freq='D')
country_data = country_data.reindex(date_index)

new_date_index = pd.date_range(max(country_data.index)-timedelta(days=29),max(country_data.index),freq='D')

for i in [3, 4, 5, 6, 7, 8]:
    for date in new_date_index:
        country_data['pred_T-'+str(i)].loc[date] = country_data['pred_T-'+str(i)].loc[date-timedelta(days=i)] * \
                                                   country_data['R0_T-'+str(i)].mean()

for i in [3, 4, 5, 6, 7, 8]:
    country_data['pred_T-' + str(i)] = country_data['pred_T-' + str(i)].astype('int64')

#plt.plot(country_data.index,country_data['T-3'])
#plt.show()

country_data.to_csv("covid19_temp/country_data_" + str(country) + ".csv")
# print(raw_data)
