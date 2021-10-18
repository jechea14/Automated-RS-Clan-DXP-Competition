from selenium import webdriver
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import csv
import pandas as pd
from skills import Skills
from pprint import pprint
from datetime import datetime

# Scrape users
def scrape():
    content = driver.page_source
    soup = BeautifulSoup(content, "html.parser")
    results = soup.find_all("table", class_="regular")[1]

    for item in results.tbody.find_all("tr")[2:]:
        username = item.find_all("td", class_="clan_td clan_rsn2")
        
        if not username:
            td = soup.new_tag('td')
            td.string="None"
            username.append(td)
            
        usr.append(username[0].get_text())

# Click to the next page    
def next_page():
    link = driver.find_element_by_link_text("next »")
    link.click()

def replace_space(url_runeclan, list):
    index = 0
    while index < len(list):
        list[index] = list[index].replace(' ', '+')
        list[index] = url_runeclan + list[index]
        index += 1
    return list

def calculate(obj_stats):
    # Calculate skills based on rules then add to new total dxp gained
    total_xp = 0.0
    halved_xp = 0.0
    doubled_xp = 0.0
    normal_xp = 0.0
    tripled_xp = 0.0
    
    for item in obj_stats:   
        if item.skill_name in normal_skills:
            normal_xp = item.dxp_gained
            total_xp += normal_xp
        elif item.skill_name in doubled_skills:
            doubled_xp = item.dxp_gained * 2.0
            total_xp += doubled_xp
        elif item.skill_name in halved_skills:
            halved_xp = item.dxp_gained / 2.0
            total_xp += halved_xp
        elif item.skill_name in tripled_skills:
            tripled_xp = item.dxp_gained * 3.0
            total_xp += tripled_xp

    return total_xp

'''
Go through each participant's runeclan page.
Scrape skill names and dxp gained.
Calculate each skill using rules applied and new total dxp gained.
'''
def scrape_data(links):
    for link in links:
        skill_stat = []
        user_stat = []   
        obj_stats = []

        driver.get(link)
        # "click" on option dropdown and select dxp gains
        select = Select(driver.find_element_by_name('dxp_col'))
        select.select_by_visible_text('DXP Live')
        
        # Scrape skills and dxp gained
        content = driver.page_source
        soup = BeautifulSoup(content, "html.parser")
        
        # User name
        name = soup.find_all("span", class_="xp_tracker_hname")[0]
        name_text = name.get_text()
        
        # Dxp
        results = soup.find_all("table", class_="regular")[0]
        
        for item in results.tbody.find_all("tr")[2:]:
            skill = item.find_all("td", class_="xp_tracker_skill")[0]
            num = item.find_all("td", class_="xp_tracker_gain xp_tracker_pos")
            if not num:
                td = soup.new_tag('td')
                td.string="0"
                num.append(td)         
            # Skill
            user_stat.append(skill.get_text())
            
            # Dxp gained in skill
            num_text = num[0].get_text()
            num_no_comma = num_text.replace(',', '')
            num_float = float(num_no_comma)
            user_stat.append(num_float)
        
        # Store each skill with xp gained in a class
        index = 0
        while index < len(user_stat):
            obj_stats.append(Skills(user_stat[index], user_stat[index+1]))
            index += 2

        total_xp = calculate(obj_stats)

        # Store user name and new total dxp gained in dict then append dict to list
        new_dxp_gains_dict = {'Name': name_text, 'DXP Gained': total_xp}
        new_dxp_gains.append(new_dxp_gains_dict)


def read_csv():
    # Open file of clan roster and append info to list of dicts
    with open('total_lvls.csv', newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            total_lvls.append(dict(row))

# Remove commas in numbers for calculations and convert string numbers to int type
def remove_commas(list):
    index = 0
    while index < len(list):
        list[index]['Total lvl'] = int(list[index]['Total lvl'].replace(',', ''))
        index += 1
    return list

'''
Check if results name matches clan roster then is placed to appropriate 
bracket based on total lvl from clan roster list.
Check to see who participated in dxp.
'''
def brackets(dxp, totals):  
    for i in range(0, len(dxp)):
        for j in range(0, len(totals)):
            if dxp[i]['Name'] == totals[j]['Name']:
                if totals[j]['Total lvl'] < 2000:
                    bracketA.append(dxp[i])
                elif totals[j]['Total lvl'] >= 2001 and totals[j]['Total lvl'] < 2300:
                    bracketB.append(dxp[i])
                elif totals[j]['Total lvl'] >= 2301 and totals[j]['Total lvl'] < 2600:
                    bracketC.append(dxp[i])
                elif totals[j]['Total lvl'] >= 2601 and totals[j]['Total lvl'] < 2700:
                    bracketD.append(dxp[i])
                elif totals[j]['Total lvl'] >= 2701 and totals[j]['Total lvl'] < 2800:
                    bracketE.append(dxp[i])
                elif totals[j]['Total lvl'] >= 2801 and totals[j]['Total lvl'] < 2850:
                    bracketF.append(dxp[i])   
                elif totals[j]['Total lvl'] >= 2851:
                    bracketG.append(dxp[i]) 

if __name__ == '__main__':
    # driver = webdriver.Chrome()
    PATH = "F:\Downloads\chromedriver_win32 (2)/chromedriver"
    driver = webdriver.Chrome(PATH)
    url = "https://www.runeclan.com/clan/Elite_Team_Killerz/xp-tracker?skill=2&criteria_set1=double_xp_weekend"
    url_runeclan = "https://www.runeclan.com/user/"
    driver.get(url)

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
    
    total_lvls = []
    usr = []
    new_dxp_gains = []
    read_csv()       
    scrape()
    # next_page()
    # scrape()    
    links = [ele for ele in usr if ele != 'None'] 
    runeclan_links = replace_space(url_runeclan, links)
    scrape_data(runeclan_links)
    driver.quit()
    totals = remove_commas(total_lvls)
    brackets(new_dxp_gains, totals)

    # sort dictionaries by DXP Gained in descending order
    bracketA_data_ordered = sorted(bracketA, key = lambda item: item['DXP Gained'], reverse=True)
    bracketB_data_ordered = sorted(bracketB, key = lambda item: item['DXP Gained'], reverse=True)
    bracketC_data_ordered = sorted(bracketC, key = lambda item: item['DXP Gained'], reverse=True)
    bracketD_data_ordered = sorted(bracketD, key = lambda item: item['DXP Gained'], reverse=True)
    bracketE_data_ordered = sorted(bracketE, key = lambda item: item['DXP Gained'], reverse=True)
    bracketF_data_ordered = sorted(bracketF, key = lambda item: item['DXP Gained'], reverse=True)
    bracketG_data_ordered = sorted(bracketG, key = lambda item: item['DXP Gained'], reverse=True)

    pprint(bracketA_data_ordered)
    pprint(bracketB_data_ordered)
    pprint(bracketC_data_ordered)
    pprint(bracketD_data_ordered)
    pprint(bracketE_data_ordered)
    pprint(bracketF_data_ordered)
    pprint(bracketG_data_ordered)

    # bracket data as dataframes for better viewing                
    bracketA_data = pd.DataFrame.from_dict(bracketA_data_ordered, orient='columns')
    bracketB_data = pd.DataFrame.from_dict(bracketB_data_ordered, orient='columns')
    bracketC_data = pd.DataFrame.from_dict(bracketC_data_ordered, orient='columns')
    bracketD_data = pd.DataFrame.from_dict(bracketD_data_ordered, orient='columns')   
    bracketE_data = pd.DataFrame.from_dict(bracketE_data_ordered, orient='columns')   
    bracketF_data = pd.DataFrame.from_dict(bracketF_data_ordered, orient='columns')   
    bracketG_data = pd.DataFrame.from_dict(bracketG_data_ordered, orient='columns')   
    
    bracketA_data['Rank'] = range(1, len(bracketA_data) + 1)
    bracketA_data = bracketA_data[list(('Rank', 'Name', 'DXP Gained'))]
    
    bracketB_data['Rank'] = range(1, len(bracketB_data) + 1)
    bracketB_data = bracketB_data[list(('Rank', 'Name', 'DXP Gained'))]
    
    bracketC_data['Rank'] = range(1, len(bracketC_data) + 1)
    bracketC_data = bracketC_data[list(('Rank', 'Name', 'DXP Gained'))]
    
    bracketD_data['Rank'] = range(1, len(bracketD_data) + 1)
    bracketD_data = bracketD_data[list(('Rank', 'Name', 'DXP Gained'))]

    bracketE_data['Rank'] = range(1, len(bracketE_data) + 1)
    bracketE_data = bracketE_data[list(('Rank', 'Name', 'DXP Gained'))]

    bracketF_data['Rank'] = range(1, len(bracketF_data) + 1)
    bracketF_data = bracketF_data[list(('Rank', 'Name', 'DXP Gained'))]

    bracketG_data['Rank'] = range(1, len(bracketG_data) + 1)
    bracketG_data = bracketG_data[list(('Rank', 'Name', 'DXP Gained'))]
    
    date = datetime.now().strftime("%m_%d_%Y")
    date_string = "results_" + date + ".xlsx"
    with pd.ExcelWriter(date_string) as writer:
        bracketA_data.to_excel(writer, sheet_name = "Bracket A < 2k Total")
        bracketB_data.to_excel(writer, sheet_name = "Bracket B 2k - 2.3k Total")
        bracketC_data.to_excel(writer, sheet_name = "Bracket C 2.3k - 2.6k Total")
        bracketD_data.to_excel(writer, sheet_name = "Bracket D 2.6k - 2.7k Total")
        bracketE_data.to_excel(writer, sheet_name = "Bracket E 2.7k - 2.8k Total")
        bracketF_data.to_excel(writer, sheet_name = "Bracket F 2.8k - 2850 Total")
        bracketG_data.to_excel(writer, sheet_name = "Bracket G > 2850 Total")