## This will run all scripts in order
## Make sure you have "covid19_temp/" folder created in the directory you're executing this file from
import time


print('Getting data ...\n')
exec(open('get_data.py').read())
print('Done\n')
print('Running compare_countries_confirmed.py ...\n')
exec(open('compare_countries_confirmed.py').read())
time.sleep(2)
print('Running compare_countries_deaths.py ...\n')
exec(open('compare_countries_deaths.py').read())

time.sleep(2)
print('Running predict_daily_growth_confirmed.py ...\n')
exec(open('predict_daily_growth_confirmed.py').read())
time.sleep(2)
print('Running predict_daily_growth_deaths.py ...\n')
exec(open('predict_daily_growth_deaths.py').read())

time.sleep(2)
print('Running compare_countries_confirmed_new_vs_total.py ...\n')
exec(open('compare_countries_confirmed_new_vs_total.py').read())
time.sleep(2)
print('Running compare_countries_deaths_new_vs_total.py ...\n')
exec(open('compare_countries_deaths_new_vs_total.py').read())