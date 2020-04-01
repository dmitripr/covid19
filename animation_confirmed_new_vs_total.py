import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Settings
columns_to_skip = 15
show_all_countries = True
top_countries_to_show = 20 # in case show_all_countries = False
greater_then_cases_to_plot = 50


raw_data = pd.read_csv('data/raw_data_confirmed_latest.csv')
cols = list(raw_data)
cols[1], cols[0] = cols[0], cols[1]
raw_data = raw_data.loc[:, cols]
raw_data = raw_data.set_index('Country/Region')
raw_data.drop(labels=['Lat', 'Long', 'Province/State'], axis=1, inplace=True)
raw_data = raw_data.groupby(level=0).sum()

counter = 1
for date in range(columns_to_skip,len(raw_data.columns)):
    day = raw_data.iloc[:, date:].columns[0]
    if show_all_countries:
        countries = raw_data[raw_data.iloc[:,date:].columns[0]].index
    else:
        countries = raw_data[raw_data.iloc[:,date:].columns[0]].sort_values(ascending=False)[:top_countries_to_show].index

    new_raw_data = raw_data.loc[countries].iloc[:,:date+1]
    new_raw_data = new_raw_data.transpose()
    as_of_date = new_raw_data.index[-1]
    new_raw_data.reset_index(drop=True, inplace=True)

    countries_collection = {}

    plt.figure(figsize=[16, 9], dpi=200)
    plt.yscale('log')
    plt.xscale('log')
    plt.grid()
    plt.scatter(1, 1, linewidths=0.1)
    plt.plot(1, 1, linewidth=0.1)
    for c in countries:
        df = pd.DataFrame(data=new_raw_data[c][new_raw_data[c] >= greater_then_cases_to_plot])
        df[c+'_new'] = np.nan
        df.reset_index(drop=True, inplace=True)
        if len(df) > 0:
            len_df = len(df)
            for i in range(6, len_df):
                df.iloc[i, 1] = df.loc[i][0] - df.loc[i - 6][0]
            if math.isnan(df[c].iloc[-1]):
                posx = 0
            else:
                posx = df[c].iloc[-1]
            if math.isnan(df[c + '_new'].iloc[-1]):
                posy = 0
            else:
                posy = df[c + '_new'].iloc[-1]
        else:
            len_df = 1
            posx = 0
            posy = 0
        countries_collection[c] = df.reset_index(drop=True)
        plt.scatter(df[c], df[c + '_new'], marker='.', linewidths=0.5)
        plt.plot(df[c], df[c + '_new'], linewidth=0.5)
        plt.text(posx, posy, c, fontsize=6, horizontalalignment='left', verticalalignment='top')
    plt.xlabel('Total Cases (log)')
    plt.ylabel('New Cases Past 6 Days (log)')
    plt.title('New Cases vs Total Confirmed Cases on '+as_of_date)
    plt.figtext(0.15, 0.115, "Data source: CSSE at JHU // Data calculations: Dmitri Prigojev", verticalalignment='bottom', horizontalalignment='left', color='grey', fontsize=7)
    plt.savefig('animation/'+str(counter).zfill(4)+'_confirmed_new_vs_total.png', dpi=200)
    plt.close()
    counter = counter + 1

print("Done")

