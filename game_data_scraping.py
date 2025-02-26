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


pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 2000)
pd.set_option('display.max_columns', 1000)
pd.set_option('max_colwidth', 2000)

# url = 'https://www.mlb.com/padres/roster'

'creat necessary folders'
baseurl = os.path.join(os.getcwd(), 'Game_Scraping')
if not os.path.exists(baseurl):
    os.makedirs(baseurl)

foldersetup = ['webpage_exports','cleaned_game_files','final_game_data']
for folder in foldersetup:
    folder_setup = os.path.join(os.getcwd(), 'Game_Scraping',folder)
    if not os.path.exists(folder_setup):
        os.makedirs(folder_setup)

'turns the webpage into lines of text stored in a list'


def grab_test_page():
    url = 'https://www.baseball-reference.com/players/gl.fcgi?id=croneja01&t=b&year=2024'
    cz = pd.DataFrame(webpage_to_list(url))
    cz.to_csv('cronenworth_2024.csv')


def clean_page_data():
    directory = os.path.join(os.getcwd(), 'Game_Scraping','webpage_exports')
    print(directory)
    for filename in os.listdir(directory):
        # print('filename is supposed to find for me: ' + filename)
        f = os.path.join(directory, filename)
        print(f)
        # print('weird os filepath thing' + str(f))
        if os.path.isfile(f):

            player_dict = {}
            results_list = []
            messyplayerdata = []
            thelist = pd.read_csv(f)

            '3. turn the page text into a big list'
            parseable = pd.DataFrame(thelist)
            '4. parse through the list and keep the essentials'
            seasongamenum = 0
            rankercount = 0
            for y in range(len(parseable)):
                '4a. find a game and create new dictionary entry'

                if 'tr id="batting_gamelogs.' in str(parseable.iloc[y][1]):
                    # print('found a row on line ' + str(y))
                    # print('found game 1 in row ' + str(y) )
                    battingrow = str(parseable.iloc[y][1]).split('>')
                    for z in range(0, len(battingrow)):
                        # print('battingrow -' + str(z))

                        'add season game # to dictionary for this game'
                        if 'data-stat="team_game_num" csk=' in battingrow[z]:
                            seasongamenum = battingrow[z + 1].replace('</td', '')
                            if "&" in seasongamenum:
                                seasongamenum = seasongamenum[0:seasongamenum.index("&")]

                            player_dict[seasongamenum] = {'Game_in_Season': seasongamenum}

                            'add lifetime game # to dictionary for this game'
                            for q in range(0, len(battingrow)):
                                if 'tr id="batting_gamelogs' in battingrow[q]:
                                    lifetimegame = battingrow[q].replace('tr id="batting_gamelogs.', '').replace('<',
                                                                                                                 '').replace(
                                        '"', '')
                                    player_dict[seasongamenum]['Lifetime_Game'] = lifetimegame

                            'add date of game to dictionary for this game'
                            for q in range(0, len(battingrow)):
                                if '<td class="left " data-stat="date_game" csk="' in battingrow[q]:
                                    gamedate = battingrow[q][45:55]
                                    player_dict[seasongamenum]['Date_of_Game'] = gamedate
                            for q in range(0, len(battingrow)):
                                # print('we made it to line 70')
                                if 'team_ID' in battingrow[q]:
                                    playerteam = battingrow[q + 1][16:19]
                                    # print(playerteam)
                                    player_dict[seasongamenum]['Player_Team'] = playerteam
                            for q in range(0, len(battingrow)):
                                # print('we made it to line 70')
                                if 'opp_ID' in battingrow[q]:
                                    oppteam = battingrow[q + 1][16:19]
                                    # print(playerteam)
                                    player_dict[seasongamenum]['Opponent_Team'] = oppteam

                            for q in range(0, len(battingrow)):
                                # print('we made it to line 70')
                                if 'game_result' in battingrow[q]:
                                    game_result = battingrow[q + 1].replace('</td', '')
                                    # print(playerteam)

                                    player_dict[seasongamenum]['Game_Result'] = game_result[0]
                                    player_dict[seasongamenum]['Final_Score'] = game_result[2:].replace('-', ' to ')

                            for q in range(0, len(battingrow)):
                                # print('we made it to line 70')
                                if 'data-stat="PA' in battingrow[q]:
                                    plate_appearances = battingrow[q + 1].replace('</td', '')
                                    # print(playerteam)
                                    player_dict[seasongamenum]['Plate_Appearances'] = plate_appearances

                            for q in range(0, len(battingrow)):
                                # print('we made it to line 70')
                                if 'data-stat="AB' in battingrow[q]:
                                    at_bats = battingrow[q + 1].replace('</td', '')
                                    # print(playerteam)
                                    player_dict[seasongamenum]['At_Bats'] = at_bats
                            for q in range(0, len(battingrow)):
                                # print('we made it to line 70')
                                if 'data-stat="R' in battingrow[q]:
                                    runs_scored = battingrow[q + 1].replace('</td', '')
                                    # print(playerteam)
                                    player_dict[seasongamenum]['Runs_Scored'] = runs_scored

                            for q in range(0, len(battingrow)):
                                # print('we made it to line 70')
                                if 'data-stat="HR' in battingrow[q]:
                                    home_runs = battingrow[q + 1].replace('</td', '')
                                    # print(playerteam)
                                    player_dict[seasongamenum]['Home_Runs'] = home_runs

                            for q in range(0, len(battingrow)):
                                # print('we made it to line 70')
                                if 'data-stat="RBI' in battingrow[q]:
                                    rbis = battingrow[q + 1].replace('</td', '')
                                    # print(playerteam)
                                    player_dict[seasongamenum]['Runs_Batted_In'] = rbis

                            for q in range(0, len(battingrow)):
                                # print('we made it to line 70')
                                if 'data-stat="SO' in battingrow[q]:
                                    strikeouts = battingrow[q + 1].replace('</td', '')
                                    # print(playerteam)
                                    player_dict[seasongamenum]['Strikeouts'] = strikeouts
            player = pd.DataFrame(player_dict)

            if len(player) == 0:
                continue
            else:

                player = player.T

                player.insert(0, "player_shortname", str(f[82:-8]), allow_duplicates=True)
                player['year'] = player.apply(lambda row: row['Date_of_Game'][0:4], axis=1)
                player['gameid'] = player.apply(
                    lambda row: row['Date_of_Game'] + '_' + row['Player_Team'] + '_' + row['Opponent_Team'], axis=1)

                player.to_csv(
                    'Game_scraping/cleaned_game_files/' + filename.replace(
                        '.csv', '') + 'games' + '.csv', )




#'5. create a dictionary, with 1 list for each row'
#  '6. use dataframe.from_dict orient=index to convert each keyvalue pair into a row'

def clean_and_combine():
    'combines yearly csvs for player game data into one per player'
    directory = os.path.join(os.getcwd(), 'Game_Scraping','cleaned_game_files')
    outputfolder = os.path.join(os.getcwd(), 'Game_Scraping','final_game_data')
    playerlist = []
    filelist = []
    'create a list of players in playerlist for each player in the directory'
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        playerurlname = filename[:-13]
        if os.path.isfile(f) and playerurlname not in playerlist:
            playerlist.append(playerurlname)
    print(playerlist)
    'for reach player in playerlist loop through all their files in directory and put them into filelist'
    for p in playerlist:
        finalfilename = os.path.join(outputfolder,str(p + '_games_final_.csv'))
        print('final file name is --- ' + finalfilename)
        for filename in os.listdir(directory):
            f = os.path.join(directory, filename)
            if p in filename:
                filelist.append(f)
        print(filelist)
        df_main = pd.DataFrame(pd.read_csv(filelist[0]))
        'for all the files for that player, combine them into one csv'
        for f in filelist[1:]:
            df_temp = pd.DataFrame(pd.read_csv(f))
            df_main = pd.concat([df_main, df_temp],ignore_index=True, sort= False)

        df_main['gameid'] = df_main.apply(lambda row:  row['gameid'] + '_GAME_' + str(row['Game_in_Season']), axis=1)
        'actually save into the big csv and reset the filelist to blank so we can do it again for the next player'
        df_main.to_csv(finalfilename)
        filelist = []

def master_game_data_file():
    directory = os.path.join(os.getcwd(), 'Game_Scraping', 'final_game_data')
    outputfolder = os.path.join(os.getcwd(), 'Game_Scraping')
    finalfilename = os.path.join(outputfolder, 'master_game_data_file.csv')
    print(finalfilename)

    filelist = []

    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        filelist.append(f)

    df_main = pd.DataFrame(pd.read_csv(filelist[0]))

    for f in filelist[1:]:
        df_temp = pd.DataFrame(pd.read_csv(f))
        df_main = pd.concat([df_main, df_temp],ignore_index=True, sort= False)
    df_main.drop(df_main.columns[df_main.columns.str.contains("unnamed", case=False)], axis=1, inplace=True)
    df_main.to_csv(finalfilename)




    # for filename in os.listdir(directory):

    #     f = os.path.join(directory, filename)
    #     print(filename[:-13])
    #
    #     if os.path.isfile(f):
    #         if os.path.isfile(filename[-13] + '.csv'):
    #             print('hi')


def grab_games(csvname, startyear, endyear):
    print('LEEROY JENKINS')
    startyear = startyear
    endyear = endyear
    player_dict = {}
    results_list = []
    messyplayerdata = []
    # folder_setup = os.path.join(os.getcwd(), 'Game_Scraping', folder)
    thelist = pd.read_csv(csvname)

    '1. create link with year'
    for p in thelist.iloc[:, 5]:
        print(p)
        playernamefix = str(p[54:]).replace('01&t=b&year=', '')
        for i in range(startyear, endyear + 1):
            # print('line 158 -----------------' + str(p)+str(i) )
            '2. go to the link to get the page text'
            time.sleep(randint(60, 180))
            print('wakey wakey -------- ' + str(p) + str(i))
            thepage = str(page_contents(str(p) + str(i)))
            # print(thepage)

            if 'we block traffic that we think is from' in thepage:
                print("we got timed out")
                quit()

            if 'Sorry, no gamelog data is available' in thepage:
                print("no gamelog data in " + str(i) + " for " + playernamefix)
                continue
            if 'Page Not Found (404 error)' in thepage:
                print("404 error for " + str(i) + " for " + playernamefix)

            else:
                '3. turn the page text into a big list and export for later cleaning'
                # print('-------------------------line 167-----------------------')
                parseable = webpage_to_list(thepage)

                parseable = pd.DataFrame(parseable)
                # print('made it out of webpage_to_list---------heres how long it is ' + str(len(parseable)))
                # parseable.to_csv(str(p)+str(i)+'.csv')
                root = 'Game_scraping'
                roottwo = 'webpage_exports'
                subdir = os.path.join(root, roottwo)
                final_path = os.path.join(subdir, thepage + '.csv')
                # playernamefix = str(p[54:]).replace('01&t=b&year=','')
                # parseable.to_csv('/Users/miles/PycharmProjects/CosmicSports/Game_scraping/webpage_exports/'+str(p[54:61])+str(i)+'.csv')
                parseable.to_csv(
                    'Game_scraping/webpage_exports/' + playernamefix + str(
                        i) + '.csv')
                # print(final_path+str(p)+str(i))


'scrapes the web for games'
# grab_games('cleaned_final_players_data.csv', 2019, 2023)
#started 4:07pm 8.8.2024

'cleans existing game date files'
# clean_page_data()

'combine each of a players annual game data files into one personal file'
# clean_and_combine()

'combines every players compilation file into a huge file'
master_game_data_file()