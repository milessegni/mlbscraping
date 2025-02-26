import numpy
import requests as requests
import selenium
import time
import os
import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 2000)
pd.set_option('display.max_columns', 1000)
pd.set_option('max_colwidth', 2000)


baseurl = os.path.join(os.getcwd(), 'Game_Scraping')
if not os.path.exists(baseurl):
    os.makedirs(baseurl)

foldersetup = ['webpage_exports','cleaned_game_files','final_game_data']
for folder in foldersetup:
    folder_setup = os.path.join(os.getcwd(), 'Game_Scraping',folder)
    if not os.path.exists(folder_setup):
        os.makedirs(folder_setup)

astrology_file = pd.read_csv(os.path.join(os.getcwd(), 'Astrology Scraping','Yearly Data','2023_daily_astrology_data.csv'))
star_sign_table = pd.read_csv(os.path.join(os.getcwd(), 'Astrology Scraping','star_signs_by_birthday.csv'))
star_sign_table = star_sign_table[['Month','Day of month','Sign']]
# print(star_sign_table.head(7))
player_file = pd.read_csv(baseurl+'/master_game_data_file.csv')
# print(player_file.head(7))
player_dob_table = pd.read_csv(os.path.join(os.getcwd(),'cleaned_final_players_data.csv'))
player_dob_table = player_dob_table[['Urlname','DOB']]
player_dob_table = player_dob_table.rename(columns={'Urlname': 'player_shortname'})
# print(player_dob_table.head(7))

'1.need to take DOB from player_dob_table and add it to player_file'
game_data_master = player_file.merge(player_dob_table, on="player_shortname")


'2. need to take star sign from star_sign_table and add it to player_file based on DOB'
'       need to make Month, Day of Month columns in the same format as the corresponding columns in star_sign_table'
game_data_master['Month'] = game_data_master.apply(lambda row: int(str(row['DOB'][0:2]).replace('/','')) if int(str(row['DOB'][0:2]).replace('/','')) > 9  else str(0)+str(row['DOB'][0:2]).replace('/',''), axis=1)
game_data_master['Day of month'] = game_data_master.apply(lambda row: row['DOB'][3:5].replace('/','') if int(str(row['Month'])) in [10,11,12]   else row['DOB'][0:4][2:].replace('/',''), axis=1)
game_data_master['Day of month'] = game_data_master.apply(lambda row: row['Day of month']             if    int(row['Day of month']) > 9   else str(0)+row['Day of month'],          axis=1)
'       star_sign_table is in int64 format. need to convert player_file date strings to match before merge'
game_data_master['Month'] = game_data_master['Month'].astype('int64')
game_data_master['Day of month'] = game_data_master['Day of month'].astype('int64')
'       merge it on down!'
game_data_master = game_data_master.merge(star_sign_table, on=['Day of month','Month'])




'3. format astrology_file to have useful columns for analysis'

astrology_file = astrology_file[['full_date','SUN','MOON', 'MERCURY','VENUS','MARS','JUPITER','SATURN','URANUS','NEPTUNE','PLUTO','NODE']]

planet_list = ['SUN','MOON', 'MERCURY','VENUS','MARS','JUPITER','SATURN','URANUS','NEPTUNE','PLUTO','NODE']
'       add a column for planet degrees, minute-weighted planet degrees, and the house the planet is currently in'

for i in planet_list:
    astrology_file[i+'_degrees'] = astrology_file[i].str[0:2].astype(int)
    astrology_file[i + '_degrees_minute_weighted'] = round((astrology_file[i].str[-2:].astype(int) / 60) * astrology_file[i + '_degrees'], 5)
    astrology_file[i + '_current_house'] = astrology_file[i].str[2:4]

'4. need to add astrology_file onto each game_master_data row'
'       format game_master_data to be in line with format of astrology_file data for merging'
game_data_master['Date_of_Game'] = game_data_master.apply(lambda row: row['Date_of_Game'].replace('-','/'),axis=1)
game_data_master['Date_of_Game'] = game_data_master['Date_of_Game'].str[5:]+'/'+game_data_master['Date_of_Game'].str[0:4]
game_data_master = game_data_master.rename(columns={'Date_of_Game': 'full_date'})
'       pick just the columns i want from astrology_file'
astrology_for_merging = astrology_file[['full_date','SUN_degrees','SUN_degrees_minute_weighted','SUN_current_house','MOON_degrees','MOON_degrees_minute_weighted','MOON_current_house','MERCURY_degrees','MERCURY_degrees_minute_weighted','MERCURY_current_house','VENUS_degrees','VENUS_degrees_minute_weighted','VENUS_current_house','MARS_degrees','MARS_degrees_minute_weighted','MARS_current_house','JUPITER_degrees','JUPITER_degrees_minute_weighted','JUPITER_current_house','SATURN_degrees','SATURN_degrees_minute_weighted','SATURN_current_house','URANUS_degrees','URANUS_degrees_minute_weighted','URANUS_current_house','NEPTUNE_degrees','NEPTUNE_degrees_minute_weighted','NEPTUNE_current_house','PLUTO_degrees','PLUTO_degrees_minute_weighted','PLUTO_current_house','NODE_degrees','NODE_degrees_minute_weighted','NODE_current_house']]


game_data_master = game_data_master.merge(astrology_for_merging, on="full_date")


print(game_data_master.head(7))

game_data_master.to_csv(baseurl+'game_data_with_planet_degrees_hottogo.csv')