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
    "Summoning",
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
    etk_data = []
    for player in arr:
        try:
            try:
                print(player + ' - hiscores ')
                req = requests.get(f'https://secure.runescape.com/m=hiscore/index_lite.ws?player={player}')

                hiscores = req.text.split('\n')
                skill_numbers = hiscores[1:29]
                split_total_lvl = hiscores[0].split(',')
                total_lvl_data = int(split_total_lvl[1])
                s = []

                for i in range(0, len(skill_numbers)):
                    s.append(skill_numbers[i].split(','))

                clanmate_data = {}
                for i in range(0, len(skill_numbers)):
                    if s[i][2] == '-1':
                        s[i][2] = 0
                    clanmate_data[skills[i]] = int(s[i][2])

                player_name = {"Name": player}
                total_lvl = {"Total Lvl": total_lvl_data}
                total_lvl.update(clanmate_data)
                player_name.update(total_lvl)
                etk_data.append(player_name)

            except:
                print(player + ' - runemetrics ')
                req = requests.get(f'https://apps.runescape.com/runemetrics/profile/profile?user={player}')
                data = req.json()
                skill_data = data["skillvalues"]
                total_lvl_data = int(data["totalskill"])
                skill_data.sort(key=myFunc)
                clanmate_data = {}

                for i in range(0, len(skill_data)):
                    clanmate_data[skills[i]] = int(skill_data[i]["xp"])

                player_name = {"Name": player}
                total_lvl = {"Total Lvl": total_lvl_data}
                total_lvl.update(clanmate_data)
                player_name.update(total_lvl)
                etk_data.append(player_name)

        except requests.ConnectionError:
            print('Connection error')

        except:
            print(f"Not found in hiscores & Runemetrics profile private: {player}. Skipping...")
            pass

    return etk_data

if __name__ == '__main__':
    players = []
    read_csv(players)
    replace_with_space(players)
    etk_data = get_player_data(players)
    write_csv(etk_data)