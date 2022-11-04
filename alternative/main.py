import requests
import pd as pandas

skills = [

    {
        "id": 0,
        "name": "Attack" 
    },
    {
        "id": 1,
        "name": "Defense"
    },
    {
        "id": 2,
        "name": "Strength"
    },
    {
        "id": 3,
        "name": "Constitution"
    },
    {
        "id": 4,
        "name": "Ranged"
    },
    {
        "id": 5,
        "name": "Prayer"
    },
    {
        "id": 6,
        "name": "Magic"
    },
    {
        "id": 7,
        "name": "Cooking"
    },
    {
        "id": 8,
        "name": "Woodcutting"
    },
    {
        "id": 9,
        "name": "Flecthing"
    },
    {
        "id": 10,
        "name": "Fishing"
    },
    {
        "id": 11,
        "name": "Firemaking"
    },
    {
        "id": 12,
        "name": "Crafting"
    },
    {
        "id": 13,
        "name": "Smithing"
    },
    {
        "id": 14,
        "name": "Mining"
    },
    {
        "id": 15,
        "name": "Herblore"
    },
    {
        "id": 16,
        "name": "Agility"
    },
    {
        "id": 17,
        "name": "Thieving"
    },
    {
        "id": 18,
        "name": "Slayer"
    },
    {
        "id": 19,
        "name": "Farming"
    },
    {
        "id": 20,
        "name": "Runecrafting"
    },
    {
        "id": 21,
        "name": "Hunter"
    },
    {
        "id": 22,
        "name": "Construction"
    },
    {
        "id": 23,
        "name": "Summmoning"
    },
    {
        "id": 24,
        "name": "Dungeoneering"
    },
    {
        "id": 25,
        "name": "Divination"
    },
    {
        "id": 26,
        "name": "Invention"
    },
    {
        "id": 27,
        "name": "Archaeology"
    }
]
 
def myFunc(e):
  return e['id']
# print(skills[0]['name'])

r = requests.get('https://apps.runescape.com/runemetrics/profile/profile?user=icekrystalx')
data = r.json()
# print(data["skillvalues"])
player_name = data["name"]


skill_data = data["skillvalues"]
skill_data1 = data["skillvalues"]

# for i in range(0, len(data["skillvalues"])):
#     skill_data.append([data["skillvalues"][i]["id"], data["skillvalues"][i]["xp"]])

# for skill in data:
#     # skill_data.append([skill["id"], skill["xp"]])
#     print(skill["skillvalues"])
skill_data.sort(key=myFunc)
skill_data1.sort(key=myFunc)

for i in range(0, len(skill_data1)):
    skill_data1[i]["skill"] = (skills[i]["name"])
print((skill_data1))