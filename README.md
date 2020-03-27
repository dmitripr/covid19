# covid19
Python scripts for extracting and calculating statistics on Covid-19 data, made available by Johns Hopkins University (JHU):
https://github.com/CSSEGISandData/COVID-19

Order of execution matters, since scripts work on CSV data stored in the `data` folder. Ensure you have `data` and `graphs` folders created before running scripts.

Use `get_data.py` to pull the dataset. 
Then run `compare_countries_confirmed.py` and `compare_countries_deaths.py` to generate the graphs and a CSV files with the related data. 
Then run `predict_daily_growth_confirmed.py` and `predict_daily_growth_deaths.py` to get predictions. 

Added `run_all_scripts.py` to execute all files automatically in order. 

Prediction calculates and uses daily change rates from available data to calculate exponential regression and predict future based on calculated coefficients.

Required python3 package libraries:
```
pandas
matplotlib
numpy
datetime
sklearn
scipy
```


Latest graphs (Will try to keep updated):
![confirmed](/graphs/corona_confirmed.png)
![deaths](/graphs/corona_deaths.png)
![predict confirmed](/graphs/predicting_confirmed.png)
![daily confirmed growth rates with regression](/graphs/rates_w_regression_confirmed.png)
![predict deaths](/graphs/predicting_deaths.png)
![daily deaths growth rates with regression](/graphs/rates_w_regression_deaths.png)