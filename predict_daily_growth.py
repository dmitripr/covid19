import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import metrics


dataset = pd.read_csv('covid19_temp/country_confirmed_comparison.csv')
countries = dataset.columns.values[1:]
countries_collection = {}


for c in countries:
    country_ds = dataset[c]
    country_ds.dropna(inplace=True)
    country_ds = country_ds.reset_index()
    country_ds['rate'] = np.nan
    for i in range(1,len(country_ds.index)):
        country_ds['rate'].at[i] = (country_ds.loc[i][1]/country_ds.loc[i-1][1])-1

    country_ds = country_ds.loc[1:].copy()

    X = country_ds['index'].values.reshape(-1,1)
    y = country_ds['rate'].values.reshape(-1,1)
    regressor = LinearRegression()
    regressor.fit(X, y)
    X_values = {}
    for n in range(len(country_ds.index)+1,len(country_ds.index)+11): X_values[n-len(country_ds.index)] = n
    X_pred = pd.DataFrame(X_values, index=[0]).transpose()
    y_pred = regressor.predict(X_pred)

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
plt.set_yscale('log')
plt.minorticks_on()
plt.set_title('Next 10 Days Totals')
plt.grid(True)
plt.set_xlabel('Days in the future')
plt.set_ylabel('Total Confirmed (log)')
plt.figure.text(0.235, 0.115, "Data source: CSSE at JHU", verticalalignment='bottom', horizontalalignment='center', color='grey', fontsize=7)
plt.figure.savefig('covid19_temp/predicting_confirmed.png', dpi=200)

print("Done")
