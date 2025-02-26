import numpy
import requests as requests
import selenium
import time
import os
import pandas as pd
from bs4 import BeautifulSoup
import requests
import unidecode
from random import randint

# url = 'https://www.mlb.com/padres/roster'
# df = pd.read_csv('padres_players_data.csv')



def page_contents(website):
    page = requests.get(website)
    print('-------------made it to page contents-------------')
    if page.status_code == 200:
        return page.text
    else:
        return page.text


'turns the webpage into lines of text stored in a list'


def webpage_to_list(website, headcleaner=''):
    temptext = ""
    counter = 0
    textlist = []
    startlogging = False

    # for i in page_contents(website):
    for i in website:

        try:
            if temptext[-1] == '\n':
                # print(temptext)
                textlist.append(temptext.strip())
                temptext = ""
            else:
                temptext += i
        except:
            temptext += i
    starthere = 0
    'this next section finds where the real content starts and deletes all the junk above it'
    # for z in range(0,len(textlist)):
    #     if '<td class="info"' in textlist[z]:
    #         starthere = z
    #         break
    # return textlist[z:]     use this if you used the text clearing thing above
    # print('------------------made it through webpage_to_list---------------')
    return textlist  # otherwise use this line


'accepts the text list from webpage_to_list and exports a cleaned dictionary of player name, jersey, DOB to CSV'


def grab_teams():
    mlbteams = 'https://www.cbssports.com/mlb/teams/'
    x = webpage_to_list(page_contents(mlbteams))
    # xdf = pd.DataFrame(x)
    teamlist = []
    for i in x:
        if '"><a href="/mlb/teams/' in i and  '/stats/" class="">Stats</a></td><td class="TableBase-bodyTd' in i:
            partone = i[26:i.index('/stats')]
            parttwo = partone.split('-')
            if parttwo[-2] == 'white' or parttwo[-2] == 'red' and len(parttwo) ==3:
                teamlist.append(str(parttwo[-2])+str(parttwo[-1]))
            else:
                teamlist.append(parttwo[-1])

    pd.DataFrame(teamlist).to_csv('all_mlb_teams.csv')






def grab_players():

    'open csv of team names'
    list_of_teams = pd.read_csv('all_mlb_teams.csv')
    list_of_teams.drop(list_of_teams.columns[list_of_teams.columns.str.contains("unnamed", case=False)], axis=1, inplace=True)

    for team in list_of_teams['0']:
        print(team)
        # 'creat url'
        teamurl = 'https://www.mlb.com/'+team+'/roster'
        'scrape the roster webpage and convert to list'
        time.sleep(randint(30, 120))
        thelist = webpage_to_list(page_contents(teamurl))
        print(str(len(thelist))+'length of scraped list for' + '------' + team)
        'run the below process on it'
        player_dict = {}
        startlogging = False
        messyplayerdata = []
        for i in range(len(thelist)):
            if '/player/' in thelist[i]:
                stringfixer = thelist[i]
                stringfixer = stringfixer.strip()
                stringfixer = stringfixer.replace('<a href="/player/', '')
                stringfixer = stringfixer.replace("</a>", '')
                stringfixer = stringfixer[8:]
                player_dict[i] = {'Name': stringfixer}

                for j in range(i + 1, len(thelist)):
                    # print(thelist[j])
                    if '</tr>' in thelist[j]:
                        # print("heres what we logged so far -----------" + str(messyplayerdata))
                        player_dict[i]['Messy_text'] = messyplayerdata
                        messyplayerdata = []
                        break
                    else:
                        if thelist[j] == '':
                            continue
                        else:
                            messyplayerdata.append(thelist[j])
        print('length of player dictionary' + str(len(player_dict))+'for the team ----------' + team)
        for k in player_dict:
            print(player_dict[k])
            for i in range(len(player_dict[k]['Messy_text'])):
                if '"jersey"' in player_dict[k]['Messy_text'][i]:
                    player_dict[k]['Messy_text'][i] = str(player_dict[k]['Messy_text'][i]).replace('<span class="jersey">',
                                                                                                   '')
                    player_dict[k]['Messy_text'][i] = str(player_dict[k]['Messy_text'][i]).replace('</span>', '')
                    player_dict[k]['Jersey'] = player_dict[k]['Messy_text'][i]

                if 'td class="birthday"' in player_dict[k]['Messy_text'][i]:
                    player_dict[k]['Messy_text'][i] = str(player_dict[k]['Messy_text'][i]).replace('<td class="birthday">',
                                                                                                   '')
                    player_dict[k]['Messy_text'][i] = str(player_dict[k]['Messy_text'][i]).replace('</td>', '')
                    player_dict[k]['DOB'] = player_dict[k]['Messy_text'][i]
                else:
                    continue
            del player_dict[k]['Messy_text']
            print('line 84' + str(player_dict[k]))
        players = pd.DataFrame(player_dict)
        players = players.T
        players.to_csv('cleaned_players_data.csv',mode='a',index=False,header=False )


'opens the cleaned player info file and adds a column for their url-friendly name and url'


def create_player_baseurl(file):
    roster = pd.read_csv(file)
    player_list = []
    'delete dashes to fit url requirements'
    roster['Name'] = roster.apply(lambda row: row['Name'].replace('-', ''), axis=1)
    roster['Name'] = roster.apply(lambda row: row['Name'].lower(), axis=1)
    roster['Name'] = roster.apply(lambda row: unidecode.unidecode(row['Name']), axis=1)

    'Add new column with their url-compatible name'
    roster['Urlname'] = roster.apply(lambda row: row['Name'].split()[1][:5], axis=1)
    roster['Urlname'] += roster.apply(lambda row: row['Name'][:2], axis=1)
    # roster['baseurl'] =  roster.apply(lambda row: str('https://www.baseball-reference.com/players/gl.fcgi?id=' + roster['Urlname'] + '01&t=b&year='), axis=1)
    # roster['baseurl'] = roster.apply(lambda row: (roster['Urlname'] + 'test'),axis=1)
    roster['baseurl'] = 'https://www.baseball-reference.com/players/gl.fcgi?id=' + roster['Urlname'] + '01&t=b&year='
    roster.to_csv('cleaned_final_players_data.csv')


# grab_players(webpage_to_list(url))
# grab_teams()
# grab_players()
# create_player_baseurl('cleaned_players_data.csv')


