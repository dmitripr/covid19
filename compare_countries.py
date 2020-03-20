import pandas as pd
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

countries = ['US', 'Germany', 'Italy', 'Korea, South', 'Iran', 'Spain', 'France']

raw_data = pd.read_csv('~/raw_data_latest.csv')
cols = list(raw_data)
cols[1], cols[0] = cols[0], cols[1]
raw_data = raw_data.loc[:, cols]

raw_data = raw_data.set_index('Country/Region')
raw_data.drop(labels=['Lat', 'Long', 'Province/State'], axis=1, inplace=True)

raw_data = raw_data.groupby(level=0).sum()
raw_data = raw_data.loc[countries]
raw_data = raw_data.transpose()
as_of_date = raw_data.index[-1]
raw_data.reset_index(drop=True, inplace=True)

countries_collection = {}

for c in countries:
    countries_collection[c] = raw_data[c][raw_data[c] > 100]
    countries_collection[c] = countries_collection[c].reset_index(drop=True)

aligned_countries = pd.concat(countries_collection, axis=1, sort=True)

aligned_countries.to_csv('country_comparison.csv')

plt.plot = aligned_countries.plot()
plt.yscale('log')
plt.minorticks_on()
plt.title('Total Confirmed Infected Since Day of First 100th Patient (As of '+as_of_date+')')
plt.grid(True)
plt.xlabel('Days Since 100th Patient')
plt.ylabel('Total Confirmed (log)')
plt.show()

print("Done")

