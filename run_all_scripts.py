## This will run all scripts in order
## Make sure you have "covid19_temp/" folder created in the directory you're executing this file from

print('Getting data ...\n')
exec(open('get_data.py').read())
print('Done\n')
print('Running compare_countries_confirmed.py ...\n')
exec(open('compare_countries_confirmed.py').read())

print('Running compare_countries_deaths.py ...\n')
exec(open('compare_countries_deaths.py').read())

print('Running predict_daily_growth_confirmed.py ...\n')
exec(open('predict_daily_growth_confirmed.py').read())

print('Running predict_daily_growth_deaths.py ...\n')
exec(open('predict_daily_growth_deaths.py').read())
