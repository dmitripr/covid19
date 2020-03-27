import pandas as pd
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

countries = ['US', 'Germany', 'Italy', 'Korea, South', 'Iran', 'Spain', 'France', 'United Kingdom', 'Brazil']
#countries = ['US', 'Germany', 'Spain', 'France', 'United Kingdom', 'Brazil', 'Russia']

raw_data = pd.read_csv('data/raw_data_confirmed_latest.csv')
cols = list(raw_data)
cols[1], cols[0] = cols[0], cols[1]
raw_data = raw_data.loc[:, cols]

raw_data = raw_data.set_index('Country/Region')
raw_data.drop(labels=['Lat', 'Long', 'Province/State'], axis=1, inplace=True)

raw_data = raw_data.groupby(level=0).sum()
# Uncomment line below if you need to output grouped data into CSV
# raw_data.to_csv('covid19_temp/raw_data_grouped_by_country.csv')
raw_data = raw_data.loc[countries]
raw_data = raw_data.transpose()
as_of_date = raw_data.index[-1]
raw_data.reset_index(drop=True, inplace=True)

countries_collection = {}

for c in countries:
    countries_collection[c] = raw_data[c][raw_data[c] > 100] # only consider data points after 100 cases has been reached
    countries_collection[c] = countries_collection[c].reset_index(drop=True)

aligned_countries = pd.concat(countries_collection, axis=1, sort=True)

aligned_countries.to_csv('data/country_confirmed_comparison.csv')

plt = aligned_countries.plot()
plt.set_yscale('log')
plt.minorticks_on()
plt.set_title('Total Confirmed Infected Since Day of First 100th Patient (As of '+as_of_date+')')
plt.grid(True)
plt.set_xlabel('Days Since 100th Patient')
plt.set_ylabel('Total Confirmed (log)')
plt.figure.text(0.15, 0.115, "Data source: CSSE at JHU // Data calculations: Dmitri Prigojev", verticalalignment='bottom', horizontalalignment='left', color='grey', fontsize=7)
plt.figure.savefig('graphs/corona_confirmed.png', dpi=200)

print("Done")

