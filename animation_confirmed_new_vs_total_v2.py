'''
by Dmitri Prigojev
Multiprocessing of graphs (version 2)
On MacOS you need to have the following environment variable set in order for this to work:
OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES
To run this in Terminal you need to first run:
export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES

After all graphs are created, use ffmpeg to compile into a movie:
ffmpeg -framerate 2 -i %04d_confirmed_new_vs_total.png -vcodec libx264 -crf 25 -pix_fmt yuv420p confirmed.mp4
'''

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
import threading
import concurrent.futures
import multiprocessing
from pandas.plotting import register_matplotlib_converters

register_matplotlib_converters()


def thread_for_plotting(raw_data, start_point, end_point, counter_i, thread_num):
    print('Thread ' + str(thread_num) + ' received:' + str(start_point) + ' ' + str(end_point) + ' ' + str(counter_i))
    for date in range(start_point, end_point + 1):
        countries = raw_data[raw_data.iloc[:, date - 1:].columns[0]].index
        print('Processing Thread ' + str(thread_num) + ' date index: ' + str(date) + '; counter: ' + str(counter_i))
        new_raw_data = raw_data.loc[countries].iloc[:, :date]
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
            df = pd.DataFrame(data=new_raw_data[c][new_raw_data[c] >= 50])
            df[c + '_new'] = np.nan
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
        plt.title('New Cases vs Total Confirmed Cases on ' + as_of_date)
        plt.figtext(0.15, 0.115, "Data source: CSSE at JHU // Data calculations: Dmitri Prigojev",
                    verticalalignment='bottom', horizontalalignment='left', color='grey', fontsize=7)
        plt.savefig('animation/' + str(counter_i).zfill(4) + '_confirmed_new_vs_total.png', dpi=200)
        plt.close()
        counter_i = counter_i + 1


def main():
    # Number of columns/days to skip in the beginning in the raw file
    columns_to_skip = 15
    # set number of processing threads to use, usually equal to the number of CPU cores on the system, can add 1
    num_threads = 5

    raw_data = pd.read_csv('data/raw_data_confirmed_latest.csv')
    cols = list(raw_data)
    cols[1], cols[0] = cols[0], cols[1]
    raw_data = raw_data.loc[:, cols]
    raw_data = raw_data.set_index('Country/Region')
    raw_data.drop(labels=['Lat', 'Long', 'Province/State'], axis=1, inplace=True)
    raw_data = raw_data.groupby(level=0).sum()

    # Divide work between the threads, sets where each thread will start and stop
    num_days = len(raw_data.columns) - columns_to_skip
    days_in_each_thread = int(num_days / num_threads)

    ranges = [[0 for i in range(2)] for j in range(num_threads)]
    counter = [1]

    day_num = columns_to_skip
    for t in range(num_threads):
        if t == 0:
            ranges[t][0] = day_num
        else:
            ranges[t][0] = day_num + 1
        ranges[t][1] = day_num + days_in_each_thread
        counter.append(((t + 1) * days_in_each_thread) + 1)
        day_num = day_num + days_in_each_thread

    # If there is a remainder in the work left over, let the last thread take care of it
    if ranges[num_threads - 1][1] < len(raw_data.columns):
        remainder = len(raw_data.columns) - ranges[num_threads - 1][1]
        ranges[num_threads - 1][1] = ranges[num_threads - 1][1] + remainder
        counter = [x + 1 for x in counter]
        # in case of remainder we want to add 1 to all counters, except the first 1 (to ensure it starts with 1)
        counter[0] = 1

    # Start the actual threads
    for i in range(num_threads):
        p = multiprocessing.Process(target=thread_for_plotting,
                                    args=(raw_data, ranges[i][0], ranges[i][1], counter[i], i))
        p.start()

    p.join()
    p.close()

    print("Done")


if __name__ == '__main__':
    main()
