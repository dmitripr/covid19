import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import metrics

def exponential(x, a, k):
    return a * np.exp(x * k)

dataset = pd.read_csv('covid19_temp/country_confirmed_comparison.csv')
days_to_predict = 10
countries = dataset.columns.values[1:]
countries_collection = {}

#get the latest date in the report
raw_data = pd.read_csv('covid19_temp/raw_data_confirmed_latest.csv')
as_of_date = raw_data.columns.values[-1]
raw_data = [] #clear memory

for c in countries:
    country_ds = dataset[c]
    country_ds.dropna(inplace=True)
    country_ds = country_ds.reset_index()
    country_ds['rate'] = np.nan
    for i in range(1,len(country_ds.index)):
        country_ds['rate'].at[i] = (country_ds.loc[i][1]/country_ds.loc[i-1][1])-1

    country_ds = country_ds.loc[1:].copy()

    X = country_ds['index'].values.flatten()
    y = country_ds['rate'].values.flatten()

    popt_exponential, pcov_exponential = scipy.optimize.curve_fit(exponential, X, y, p0=[0.5, -0.1])

    X_values = {}
    for n in range(len(country_ds.index)+1,len(country_ds.index)+days_to_predict+1): X_values[n-len(country_ds.index)] = n
    X_pred = pd.DataFrame(X_values, index=[0]).transpose()
    X_pred['pred_y'] = X_pred.apply(lambda x: exponential(x[0], popt_exponential[0], popt_exponential[1]), axis=1)
    y_pred = X_pred['pred_y'].values.flatten()

    country_ds_pred = country_ds.iloc[-1:,].copy()
    country_ds_pred = pd.concat([country_ds_pred,pd.DataFrame(y_pred)],axis=0)
    country_ds_pred.reset_index(drop=True, inplace=True)

    for i in range(0,len(country_ds_pred)-1):
        country_ds_pred.iloc[i+1,1] = country_ds_pred.iloc[i,1]*(1+country_ds_pred.iloc[i+1,0])

    country_ds_pred.drop(labels=[0,'index','rate'], inplace=True, axis=1)
    countries_collection[c] = country_ds_pred[c]

aligned_countries = pd.concat(countries_collection, axis=1, sort=True)

aligned_countries.to_csv('covid19_temp/predict_daily_growth_confirmed_comparison.csv')

plt = aligned_countries.plot()
plt.minorticks_on()
plt.set_title('Next '+str(days_to_predict)+' Days Confirmed Totals (As of '+as_of_date+')')
plt.grid(True)
plt.set_xlabel('Days in the future')
plt.set_ylabel('Total Confirmed (Millions)')
plt.figure.text(0.15, 0.115, "Data source: CSSE at JHU // Data calculations: Dmitri Prigojev", verticalalignment='bottom', horizontalalignment='left', color='grey', fontsize=7)
plt.figure.savefig('covid19_temp/predicting_confirmed.png', dpi=200)

print("Done")
