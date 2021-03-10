from selenium import webdriver
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import csv
# import pandas as pd
from pprint import pprint

PATH = "/Users/jeanie/Downloads/chromedriver"
driver = webdriver.Chrome(PATH)
url = "https://www.runeclan.com/clan/Elite_Team_Killerz/xp-tracker/1?skill=2&criteria_set1=double_xp_weekend"
driver.get(url)

bracketA = []
bracketB = []
bracketC = []
bracketD = []
total_lvls = []
usr = []

def scrape():
    content = driver.page_source
    soup = BeautifulSoup(content, "html.parser")
    results = soup.find_all("table", class_="regular")[1]

    # scrape users
    for item in results.tbody.find_all("tr")[2:]:
        username = item.find_all("td", class_="clan_td clan_rsn2")
        dxp = item.find_all("td", class_="clan_td clan_xpgain_trk")
        
        if not username:
            td = soup.new_tag('td')
            td.string="None"
            username.append(td)
        if not dxp:
            td = soup.new_tag('td')
            td.string="None"
            dxp.append(td)
            
        usr.append(username[0].get_text())
        usr.append(dxp[0].get_text())

def next_page():
    # click to the next page    
    link = driver.find_element_by_link_text("next »")
    link.click()

def make_new_gains_dict(res):
    dxp_gains = []
    index = 0
    while index < len(res):
        new_dxp_gains_dict = {'Name': res[index], 'DXP Gained': res[index+1]}
        dxp_gains.append(new_dxp_gains_dict)
        index += 2
    return dxp_gains
        
def remove_commas(list):
    #remove commas in numbers for calculations and convert string numbers to int type
    index = 0
    while index < len(list):
        list[index]['Total lvl'] = int(list[index]['Total lvl'].replace(',', ''))
        index += 1
    return list

def brackets(dxp, totals):  
    # check if results name matches clan roster then is placed to appropriate bracket based on total lvl from clan roster list
    # check to see who participated in dxp
    for i in range(0, len(dxp_gains)):
        for j in range(0, len(totals)):
            if dxp_gains[i]['Name'] == totals[j]['Name']:
                if totals[j]['Total lvl'] < 2000:
                    bracketA.append(dxp_gains[i])
                elif totals[j]['Total lvl'] >= 2000 and totals[j]['Total lvl'] < 2500:
                    bracketB.append(dxp_gains[i])
                elif totals[j]['Total lvl'] >= 2500 and totals[j]['Total lvl'] < 2700:
                    bracketC.append(dxp_gains[i])
                elif totals[j]['Total lvl'] >= 2700:
                    bracketD.append(dxp_gains[i]) 

def read_csv():                    
    # open file of clan roster and append info to list of dicts
    with open('total_lvls.csv', newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            total_lvls.append(dict(row))
 
read_csv()       
scrape()
next_page()
scrape()
res = [ele for ele in usr if ele != 'None'] 
dxp_gains = make_new_gains_dict(res)
totals = remove_commas(total_lvls)
brackets(dxp_gains, totals)

pprint(bracketA)
pprint(bracketB)
pprint(bracketC)
pprint(bracketD)
               
# # bracket data as dataframes for better viewing                
# bracketA_data = pd.DataFrame.from_dict(bracketA, orient='columns')
# bracketB_data = pd.DataFrame.from_dict(bracketB, orient='columns')
# bracketC_data = pd.DataFrame.from_dict(bracketC, orient='columns')
# bracketD_data = pd.DataFrame.from_dict(bracketD, orient='columns')  
driver.quit()

# from selenium import webdriver
# from selenium.webdriver.support.ui import Select
# from bs4 import BeautifulSoup
# import csv
# import pandas as pd
# from skills import Skills
# from pprint import pprint
# PATH = "/Users/jeanie/Downloads/chromedriver"
# driver = webdriver.Chrome(PATH)

# url = "https://www.runeclan.com/clan/Elite_Team_Killerz/xp-tracker/1?skill=2&criteria_set1=double_xp_weekend"

# driver.get(url)

# content = driver.page_source
# soup = BeautifulSoup(content, "html.parser")

# bracketA = []
# bracketB = []
# bracketC = []
# bracketD = []
# total_lvls = []

# results = soup.find_all("table", class_="regular")[1]

# # scrape users
# usr = []

# for item in results.tbody.find_all("tr")[2:]:
#     username = item.find_all("td", class_="clan_td clan_rsn2")
#     dxp = item.find_all("td", class_="clan_td clan_xpgain_trk")
    
#     if not username:
#         td = soup.new_tag('td')
#         td.string="None"
#         username.append(td)
#     if not dxp:
#         td = soup.new_tag('td')
#         td.string="None"
#         dxp.append(td)
        
#     usr.append(username[0].get_text())
#     usr.append(dxp[0].get_text())
    
# # click to the next page    
# link = driver.find_element_by_link_text("next »")
# link.click()

# # scrape usernames on next page
# content1 = driver.page_source
# soup1 = BeautifulSoup(content1, "html.parser")
# results1 = soup1.find_all("table", class_="regular")[1]

# for item in results1.tbody.find_all("tr")[2:]:
#     username = item.find_all("td", class_="clan_td clan_rsn2")
#     dxp = item.find_all("td", class_="clan_td clan_xpgain_trk")
    
#     if not username:
#         td = soup.new_tag('td')
#         td.string="None"
#         username.append(td)
#     if not dxp:
#         td = soup.new_tag('td')
#         td.string="None"
#         dxp.append(td)
        
#     usr.append(username[0].get_text())
#     usr.append(dxp[0].get_text())

# res = [ele for ele in usr if ele != 'None'] 

# dxp_gains = []

# # print(res)

# index = 0
# while index < len(res):
#     new_dxp_gains_dict = {'Name': res[index], 'DXP Gained': res[index+1]}
#     dxp_gains.append(new_dxp_gains_dict)
#     index += 2
    
# print(dxp_gains)

# # open file of clan roster and append info to list of dicts
# with open('total_lvls.csv', newline='', encoding='utf-8-sig') as csvfile:
#     reader = csv.DictReader(csvfile)
#     for row in reader:
#         total_lvls.append(dict(row))

# #remove commas in numbers for calculations and convert string numbers to int type
# index = 0
# while index < len(total_lvls):
#     total_lvls[index]['Total lvl'] = int(total_lvls[index]['Total lvl'].replace(',', ''))
#     index += 1

# # check if results name matches clan roster then is placed to appropriate bracket based on total lvl from clan roster list
# # check to see who participated in dxp
# for i in range(0, len(dxp_gains)):
#     for j in range(0, len(total_lvls)):
#         if dxp_gains[i]['Name'] == total_lvls[j]['Name']:
#             if total_lvls[j]['Total lvl'] < 2000:
#                 bracketA.append(dxp_gains[i])
#             elif total_lvls[j]['Total lvl'] >= 2000 and total_lvls[j]['Total lvl'] < 2500:
#                 bracketB.append(dxp_gains[i])
#             elif total_lvls[j]['Total lvl'] >= 2500 and total_lvls[j]['Total lvl'] < 2700:
#                 bracketC.append(dxp_gains[i])
#             elif total_lvls[j]['Total lvl'] >= 2700:
#                 bracketD.append(dxp_gains[i]) 
                
# # bracket data as dataframes for better viewing                
# bracketA_data = pd.DataFrame.from_dict(bracketA, orient='columns')
# bracketB_data = pd.DataFrame.from_dict(bracketB, orient='columns')
# bracketC_data = pd.DataFrame.from_dict(bracketC, orient='columns')
# bracketD_data = pd.DataFrame.from_dict(bracketD, orient='columns')  
# driver.quit()