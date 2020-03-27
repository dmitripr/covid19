import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy
import math
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import metrics

def exponential(x, a, k):
    return a * np.exp(x * k)

dataset = pd.read_csv('covid19_temp/country_deaths_comparison.csv')
days_to_predict = 10
countries = dataset.columns.values[1:]
countries_collection = {}
curve_fit_collection = {}

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
    country_ds['curve_fit'] = country_ds.apply(lambda x: exponential(x['index'], popt_exponential[0], popt_exponential[1]), axis=1)

    # Calculate R squared of the regression line
    residuals = y - exponential(X, popt_exponential[0], popt_exponential[1])
    ss_res = np.sum(residuals ** 2)
    ss_tot = np.sum((y - np.mean(y)) ** 2)
    r_squared = round(1 - (ss_res / ss_tot), 3)

    # Copy plot data and the fit line into the collection and set the name to include R squared, to be displayed later
    curve_fit_collection[c + str(' (R^2=') + str(r_squared) + str(')')] = country_ds

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
aligned_countries = aligned_countries.round(0)
aligned_countries.to_csv('covid19_temp/predict_daily_growth_deaths_comparison.csv')

graph = aligned_countries.plot()
graph.minorticks_on()
graph.set_title('Next '+str(days_to_predict)+' Days Death Totals (As of '+as_of_date+')')
graph.grid(True)
graph.set_xlabel('Days in the future')
graph.set_ylabel('Total Deaths')
graph.figure.text(0.15, 0.115, "Data source: CSSE at JHU // Data calculations: Dmitri Prigojev", verticalalignment='bottom', horizontalalignment='left', color='grey', fontsize=7)
graph.figure.savefig('covid19_temp/predicting_deaths.png', dpi=200)


n = 1
num_graph_rows = math.ceil(len(curve_fit_collection)/3)
plt.figure(dpi=200)
plt.suptitle('Daily Growth Rates of Deaths with Regression (As of '+as_of_date+')')
for curve in curve_fit_collection:
    plt.subplot(num_graph_rows, 3, n, yticklabels='', xticklabels='', xticks=[], yticks=[])
    plt.plot(curve_fit_collection[curve]['index'].values, curve_fit_collection[curve]['rate'].values)
    plt.plot(curve_fit_collection[curve]['index'].values, curve_fit_collection[curve]['curve_fit'].values)
    plt.title(curve, fontsize=8)
    n = n + 1
plt.figtext(0.05, 0.05, "Data source: CSSE at JHU // Data calculations: Dmitri Prigojev", verticalalignment='bottom', horizontalalignment='left', color='grey', fontsize=7)
plt.savefig('covid19_temp/rates_w_regression_deaths.png')


print("Done")
