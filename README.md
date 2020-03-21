# covid19
Python scripts for extracting and calculating statistics on Covid-19 data, made available by Johns Hopkins University (JHU):
https://github.com/CSSEGISandData/COVID-19


Use `get_data.py` to pull the dataset, then run `compare_countries_confirmed.py` and `compare_countries_deaths.py` to generate the graphs and a CSV file with the related data. 

Required python3 package libraries:
```
pandas
matplotlib
numpy
datetime
```
Sample graphs:
![confirmed](/corona_confirmed.png)
![deaths](/corona_deaths.png)
