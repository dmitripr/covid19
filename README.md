# covid19
Python scripts for extracting and calculating statistics on Covid-19 data, made available by Johns Hopkins University (JHU):
https://github.com/CSSEGISandData/COVID-19

Order of execution matters, since scripts work on CSV data stored in the `data` folder. Ensure you have `data` and `graphs` folders created before running scripts.

Use `get_data.py` to pull the dataset. 
Then run `compare_countries_confirmed.py` and `compare_countries_deaths.py` to generate the graphs and a CSV files with the related data. 
Then run `predict_daily_growth_confirmed.py` and `predict_daily_growth_deaths.py` to get predictions. 

Added `run_all_scripts.py` to execute all files automatically in order. 

Prediction calculates and uses daily change rates from available data to calculate exponential regression and predict future based on calculated coefficients.
The number of days regression calculation considers is controlled by a `days_for_regression` variable in the `predict_*` files.

Required python3 package libraries:
```
pandas
matplotlib
numpy
datetime
sklearn
scipy
```

**Animation**

Animation it done by running `animation_confirmed_new_vs_total.py`, this script uses data gathered by `get_data.py`. It will place individual plots into `animation` folder.
After all plots are created you can run `ffmpeg` to generate MP4 file. I use the following command:

`ffmpeg -framerate 2 -i %04d_confirmed_new_vs_total.png -vcodec libx264 -crf 25  -pix_fmt yuv420p confirmed.mov`

I added multiprocessing capability to version 2 (`animation_confirmed_new_vs_total_v2.py` & `animation_deaths_new_vs_total_v2.py`)

If you are using MacOS you need to have the following environment variable set in order for this to work:
`OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES`

To run this in Terminal you need to first run: `export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES`

### Latest graphs (will try to keep updated):

**Link to animation of confirmed cases MP4:** 
[Confirmed](https://github.com/dmitripr/covid19/blob/master/animation/confirmed.mov?raw=true)
[Deaths](https://github.com/dmitripr/covid19/blob/master/animation/deaths.mov?raw=true)

![confirmed new vs total](/graphs/confirmed_new_vs_total.png)
![deaths new vs total](/graphs/deaths_new_vs_total.png)
![confirmed](/graphs/corona_confirmed.png)
![deaths](/graphs/corona_deaths.png)
![predict confirmed](/graphs/predicting_confirmed.png)
![daily confirmed growth rates with regression](/graphs/rates_w_regression_confirmed.png)
![predict deaths](/graphs/predicting_deaths.png)
![daily deaths growth rates with regression](/graphs/rates_w_regression_deaths.png)