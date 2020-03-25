# covid19
Python scripts for extracting and calculating statistics on Covid-19 data, made available by Johns Hopkins University (JHU):
https://github.com/CSSEGISandData/COVID-19

Order of execution matters, since scripts work on CSV data stored in the `covid19_temp` folder.

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


Sample graphs (Will try to keep updated):
![confirmed](/covid19_temp/corona_confirmed.png)
![deaths](/covid19_temp/corona_deaths.png)
![predict confirmed](/covid19_temp/predicting_confirmed.png)
![predict deaths](/covid19_temp/predicting_deaths.png)
