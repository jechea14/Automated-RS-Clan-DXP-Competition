import csv
import pandas as pd

def read_csv(arr, csv_file):
    with open(csv_file, newline='', encoding= 'unicode_escape') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            arr.append(dict(row))

if __name__ == '__main__':
    CSV1 = 'clanmate_data1_11_05_2022.csv'

    a1 = []
    read_csv(a1, CSV1)
    df = pd.DataFrame.from_dict(data=a1)
    print(df)

    bracketA = []
    bracketB = []
    bracketC = []
    bracketD = []
    bracketE = []
    bracketF = []
    bracketG = []

    halved_skills = [
        'Attack',
        'Defence',
        'Strength',
        'Constitution',
        'Ranged',
        'Magic',
        'Summoning',
        'Herblore',
        'Farming',
        'Invention',
        'Archaeology',
        'Dungeoneering'
    ]

    normal_skills = [
        'Fletching',
        'Crafting',
        'Thieving'
    ]

    doubled_skills = [
        'Hunter',
        'Smithing',
        'Firemaking',
        'Prayer',
        'Cooking',
        'Slayer',
        'Construction'
    ]

    tripled_skills = [
        'Agility',
        'Divination',
        'Fishing',
        'Woodcutting',
        'Mining',
        'Runecrafting'
    ]