import requests
import csv
import pandas as pd
from datetime import datetime

skills = [
    "Attack" ,
    "Defense",
    "Strength",
    "Constitution",
    "Ranged",
    "Prayer",
    "Magic",
    "Cooking",
    "Woodcutting",
    "Fletching",
    "Fishing",
    "Firemaking",
    "Crafting",
    "Smithing",
    "Mining",
    "Herblore",
    "Agility",
    "Thieving",
    "Slayer",
    "Farming",
    "Runecrafting",
    "Hunter",
    "Construction",
    "Summmoning",
    "Dungeoneering",
    "Divination",
    "Invention",
    "Archaeology"
]
 
def myFunc(e):
  return e['id']

def read_csv(arr):
    with open('members_lite.csv', newline='', encoding= 'unicode_escape') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            arr.append(row['Clanmate'])

def write_csv(obj):
    date = datetime.now().strftime("%m_%d_%Y")
    date_string = "clanmate_data_" + date + ".csv"
    df = pd.DataFrame.from_dict(data=obj)
    df.to_csv(date_string)

def replace_with_space(arr):
    index = 0
    while index < len(arr):
        arr[index] = arr[index].replace('\xa0', ' ')
        index += 1

def get_player_data(arr):
    c = []
    for player in arr:
        try:
            try:
                print(player)
                req = requests.get(f'https://secure.runescape.com/m=hiscore/index_lite.ws?player={player}')

                hiscores = req.text.split('\n')
                skil = hiscores[1:29]
                s = []

                for i in range(0, len(skil)):
                    
                    s.append(skil[i].split(','))

                a = {}
                for i in range(0, len(skil)):
                    if s[i][2] == '-1':
                        s[i][2] = '0'
                    a[skills[i]] = (s[i][2])

                b = {"Name": player}
                b.update(a)
                c.append(b)

            except:
                print(player)
                req = requests.get(f'https://apps.runescape.com/runemetrics/profile/profile?user={player}')
                data = req.json()
                skill_data = data["skillvalues"]

                skill_data.sort(key=myFunc)

                a = {}

                for i in range(0, len(skill_data)):
                    a[skills[i]] = (skill_data[i]["xp"])
                b = {"Name": player}
                b.update(a)
                c.append(b)

        except:
            print(f"Not found in hiscores & Runemetrics profile private: {player}. Skipping...")
            pass

    return c

if __name__ == '__main__':

    players = []
    read_csv(players)
    replace_with_space(players)
    player = get_player_data(players)
    write_csv(player)



