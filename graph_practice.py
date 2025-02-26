import matplotlib.pyplot as plt
import numpy as np
import requests as requests
import selenium
import time
import os
import pandas as pd
from bs4 import BeautifulSoup
import requests
import unidecode

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 2000)
pd.set_option('display.max_columns', 1000)
pd.set_option('max_colwidth', 2000)

df =     pd.read_csv('C:/Users/miles/PycharmProjects/CosmicSports/Game_scraping/final_game_data/kimha_games_final_.csv')
# df = df.DataFrame('kimha_games_final_.csv')

# plot = df.plot.scatter(x=df['year'],
#                        y=df['At_Bats']
#                        )
# print(df['year'])


# df['year'].plot()

# df.plot.scatter(x="Opponent_Team", y="Runs_Batted_In", alpha=0.5)

# df.hist(column='Runs_Batted_In', by='year')


def percenthistogram():
    ' percentage histogram'
    plt.hist(df['Runs_Batted_In'], density=True, weights=np.ones(len(df['Runs_Batted_In'])) / len(df['Runs_Batted_In']) * 100)
    plt.ylabel('Percentage')
    plt.show()

def pivot_time():

    new_table = pd.pivot_table(df, values=['Runs_Batted_In'], index=['year'],
                           # columns=['Please select your gender.'],
                               aggfunc="sum")

    return new_table




def linechart():
    'line chart with player batting average per year?'
    yearruns = df.groupby(by='year').sum('Runs_Batted_in')
    #get rid of junk columns
    yearruns['year'] = yearruns.index

    yearruns['avg_rbi'] = yearruns['Runs_Batted_In'] / yearruns['At_Bats']
    yearruns.plot(y='avg_rbi',kind='line',x='year')
    plt.xticks(yearruns['year'])
    print(yearruns)
    plt.show()

# percenthistogram()
# ez = pivot_time()
# newchart = ez.plot()
# plt.xticks(ez.index)
# plt.show()