import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

countries = ['US', 'Germany', 'Italy', 'Russia', 'Iran', 'Spain', 'France', 'United Kingdom', 'Brazil']
#countries = ['US', 'Germany', 'Spain', 'France', 'United Kingdom', 'Brazil', 'Russia']

raw_data = pd.read_csv('data/raw_data_deaths_latest.csv')
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

plt.figure(dpi=200)
plt.yscale('log')
plt.xscale('log')
plt.grid()
for c in countries:
    df = pd.DataFrame(data=raw_data[c][raw_data[c] > 1])
    df[c+'_new'] = np.nan
    df.reset_index(drop=True, inplace=True)
    for i in range(6,len(df)):
        df.iloc[i, 1] = df.loc[i][0] - df.loc[i-6][0]
    countries_collection[c] = df.reset_index(drop=True)
    plt.scatter(df[c], df[c + '_new'], marker='.', linewidths=0.5)
    plt.plot(df[c], df[c + '_new'], linewidth=0.5)
    plt.text(df[c].iloc[-1], df[c + '_new'].iloc[-1], c, fontsize=6, horizontalalignment='left', verticalalignment='top')
#plt.legend(countries)
plt.xlabel('Total Deaths (log)')
plt.ylabel('New Deaths Past 6 Days (log)')
plt.title('New Deaths vs Total Deaths (As of '+as_of_date+')')
plt.figtext(0.15, 0.115, "Data source: CSSE at JHU // Data calculations: Dmitri Prigojev", verticalalignment='bottom', horizontalalignment='left', color='grey', fontsize=7)
plt.savefig('graphs/deaths_new_vs_total.png', dpi=200)

print("Done")

