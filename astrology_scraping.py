import csv

import numpy
import requests as requests
import selenium
import time
import os
import pandas as pd
from bs4 import BeautifulSoup
import requests
from padre_scraping import page_contents
from padre_scraping import webpage_to_list
from random import randint
from urllib.request import Request, urlopen
import pathlib

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 2000)
pd.set_option('display.max_columns', 1000)
pd.set_option('max_colwidth', 2000)

# baseurl = str(os.getcwd()).replace(r'"\\"','/')
'we really are out here'
'i am commenting on the local Miles and attempting to commit and push to the server miles'

baseurl = os.path.join(os.getcwd(), 'Astrology Scraping', 'Raw Exports')
if not os.path.exists(baseurl):
    os.makedirs(baseurl)



months = ['JANUARY', 'FEBRUARY', 'MARCH', 'APRIL', 'MAY', 'JUNE', 'JULY', 'AUGUST', 'SEPTEMBER', 'OCTOBER', 'NOVEMBER',
          'DECEMBER']
month_numbers = {'JANUARY': '01', 'FEBRUARY': '02', 'MARCH': '03', 'APRIL': '04', 'MAY': '05', 'JUNE': '06',
                 'JULY': '07', 'AUGUST': '08', 'SEPTEMBER': '09',
                 'OCTOBER': '10', 'NOVEMBER': '11', 'DECEMBER': '12'}


def get_ephermis_data(start, end):
    for i in range(start, end + 1):
        print(i)
        urlformat = 'https://www.findyourfate.com/astrology/ephemeris/' + str(i) + '.html'
        print(urlformat)
        time.sleep(randint(30, 60))
        cz = webpage_to_list(page_contents(urlformat))

        cz = pd.DataFrame(cz)
        cz.to_csv('Astrology Scraping/Raw Exports/astrology_data' + str(i) + '.csv')


def clean_astrology_year_export():
    list_of_monthly_lists = []
    temp_row_holder = []
    zefolder = baseurl
    for filename in os.listdir(zefolder):
        print(filename)
        f = os.path.join(zefolder, filename)
        if os.path.isfile(f):
            print(f)
            df = pd.read_csv(f)
            print(len(df))
            # temp_row_holder = []
            # list_of_monthly_lists = []
            '1. identify year of file'
            zeyear = str(f)[-8:][:4]
            # print(zeyear)

            'create yearly dataframe for all the individual months to be added to'
            year_output_temp = pd.DataFrame(
                columns=['DATE', 'SID.TIME', 'SUN', 'MOON', 'MERCURY', 'VENUS', 'MARS', 'JUPITER', 'SATURN', 'URANUS',
                         'NEPTUNE', 'PLUTO', 'NODE'])

            '2. loop through months in the year and grab data'
            for i in months:
                currentmonth = str(i) + ' ' + zeyear
                temp_row_holder = []
                # print(currentmonth)
                logjam = False

                for y in range(len(df)):

                    if currentmonth in str(df.iloc[y][1]):
                        logjam = True
                        # temp_row_holder.append(str(df.iloc[y][1]))
                        print('found the month on line ---------' + currentmonth + '-----' + str(y))

                    if logjam is True and currentmonth not in str(df.iloc[y][1]) and 'FF9900' not in str(df.iloc[y][1]):
                        temp_row_holder.append(str(df.iloc[y][1]))
                        # print('appended to temp row holder, line ---------' + str(y) + '---------------' + str(df.iloc[y][1]))
                    'dynamically find the table ending characters and wrap up the month'
                    if '</p>' in str(df.iloc[y][1]) and logjam is True:

                        # temp_row_holder.append(str(df.iloc[y][1]))
                        logjam = False
                        print('table ending character found on line ------' + str(y))
                        'clear out header junk (fixed)'
                        # del temp_row_holder[0:2]

                        for h in range(0, len(temp_row_holder) - 1):
                            'wrap up: clear out header junk (fixed)'
                            temp_row_holder[h] = temp_row_holder[h].replace('<b style="color:#FF9900">', '')
                            temp_row_holder[h] = temp_row_holder[h].replace('</b>', '')
                            temp_row_holder[h] = temp_row_holder[h].replace('<p> ', '')
                            temp_row_holder[h] = temp_row_holder[h].replace('<p>', '')
                            temp_row_holder[h] = temp_row_holder[h].replace('p>', '')
                            # print(temp_row_holder[h])
                        'delete the first two list entries which are just headers'
                        # rows_to_delete = []
                        h = 0
                        while h < len(temp_row_holder) - 1:
                            if temp_row_holder[h] == 'div class="ephetxt">' or temp_row_holder[h] == 'nan' or temp_row_holder[h] == 'pre>':
                                print('found a culprit-----------' + temp_row_holder[h])
                                del temp_row_holder[h]
                                continue
                            h += 1
                            print(h)

                        for m in range(0, len(temp_row_holder)):
                            'wrap up: remove the first space in the first column of each list entry so it becomes space-separated'
                            temp_row_holder[m] = temp_row_holder[m][0:5].replace(' ', '_') + " " + temp_row_holder[m][
                                                                                                   6:]
                            if '<' in temp_row_holder[m]:
                                temp_row_holder[m] = temp_row_holder[m][0:temp_row_holder[m].find("<")]
                            # if 'div class="ephetxt">' or 'nan' or 'pre>' in temp_row_holder[m]:
                            #     del temp_row_holder[m]
                        for q in range(0, len(temp_row_holder)):
                            temp_row_holder[q] = month_numbers[i] + ' ' + zeyear + ' ' + temp_row_holder[q]
                            temp_row_holder[q] = temp_row_holder[q].split()
                        list_of_monthly_lists.append(temp_row_holder)

                        break
            # print(temp_for_csv.columns)

        ' once done cleaning convert to a dataframe and append it to the master dataframe for that year'
    df_main = pd.DataFrame(list_of_monthly_lists[0],
                           columns=['month', 'year', 'DATE', 'SID.TIME', 'SUN', 'MOON', 'MERCURY',
                                    'VENUS', 'MARS', 'JUPITER', 'SATURN', 'URANUS',
                                    'NEPTUNE', 'PLUTO', 'NODE'])

    # print(len(df_main))
    # print(len(list_of_monthly_lists))

    for f in range(1, len(list_of_monthly_lists)):
        print('ok i made it to list number -----------' + str(f))
        df_temp = pd.DataFrame(list_of_monthly_lists[f],
                               columns=['month', 'year', 'DATE', 'SID.TIME', 'SUN', 'MOON', 'MERCURY',
                                        'VENUS', 'MARS', 'JUPITER', 'SATURN', 'URANUS',
                                        'NEPTUNE', 'PLUTO', 'NODE'])
        df_main = pd.concat([df_main, df_temp], ignore_index=True, sort=False)

    df_main['full_date'] = df_main.apply(
        lambda row: str(row['month']) + '/' + str(row['DATE'][3:]) + '/' + str(row['year']), axis=1)
    yearlypath = 'Astrology Scraping/Yearly Data/'
    if not os.path.exists(yearlypath) :
        os.makedirs('Astrology Scraping/Yearly Data/')
    df_main.to_csv('Astrology Scraping/Yearly Data/' + zeyear + '_daily_astrology_data.csv')


'ooga booga'
# get_ephermis_data(2020,2023)
# clean_astrology_year_export()
# print(pathlib.Path("padres_players_data.csv").parent.absolute())
