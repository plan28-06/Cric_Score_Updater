import requests # We use requests module to get the HTML structure of the desired URL
from bs4 import BeautifulSoup
from termcolor import colored
import selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium import webdriver # webdriver makes use of browser API and helps us mimic a human interacting with the browser
import time
from selenium.webdriver.chrome.service import Service



scrap_URL = "https://www.cricbuzz.com"

def overview():
    resp = requests.get(scrap_URL)
    soup = BeautifulSoup(resp.content,'html5lib') 
    #html5lib is a parser that goes through the raw html and convertes it to a structured tree form
    # which is traversed by beautiful soup to get us our desired content (we use of dedicated parser for simple navigation)

    table = soup.find_all('li', attrs = {'class': 'cb-view-all-ga cb-match-card cb-bg-white'}) # gets list of matches displayed in hom page
    pref = 'IND' # replace this with desired initial (IND -> India)

    for li in table:
        match = li.text.strip()
        if(match.count(pref)>0):
            print(colored(match, 'magenta'))
            link = li.find('a')
            print('\n')
            return link['href'], match


def fetch_details(link):
    url = link
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html5lib')
    stats = soup.find('div', attrs = {'class': 'cb-col-67 cb-col'})
    scores = stats.find_all('div')
    table = []
    cnt = 0
    row = {}
    for s in scores:
        if(cnt%6==0 and len(row)): # Once all 6 details have been added to row , we append it to table
            table.append(row)
            row = {} 
        if(len(s.find_all('div'))==0): # Condition for leaf elements (elements with no children)
            cnt+=1
            row[(cnt-1)%6]=s.text.strip()
    table.append(row)  
    batter = False
    message = ''
    for row in table:
        if(row[0]=='Batsman' or row[0]=='Bowler'):
            print(colored("{:<24} {:<8} {:<8} {:<8} {:<8} {:<8}".format(row[0], row[1], row[2], row[3], row[4], row[5]), 'cyan', attrs=['bold']))
            batter = not batter
        else:
            print(colored("{:<24} {:<8} {:<8} {:<8} {:<8} {:<8}".format(row[0], row[1], row[2], row[3], row[4], row[5]), 'white'))
            if(batter):
                msg = '\n'+row[0]+':  '+row[1]+'('+row[2]+')'+'  '+'S.R. '+row[5]
                message += msg
            else:
                msg = '\n'+row[0]+':  '+row[1]+'-'+row[2]+'-'+row[3]+'-'+row[4]
                message += msg
    return message

meow = overview()

msg = fetch_details(scrap_URL+meow[0])
print(msg) 


# Sending the scrapped data via whatsapp
chrome_driver_path = r"C:\Users\plana\Downloads\chromedriver.exe"
service = Service(chrome_driver_path)
browser = webdriver.Chrome(service=service)# It creates an instance of the Chrome WebDriver,
# which is a tool that allows you to automate and control the Google Chrome browser.

URL = 'https://web.whatsapp.com/'
browser.get(URL) # Opens the webage

time.sleep(10)


def send_message(rec, mes, browser):
    try:
        search_bar = browser.find_element(By.XPATH, '//*[@id="side"]/div[1]/div/div[2]/div[2]/div/div')# relative xpath of anything that is editable by the user
        search_bar.send_keys(rec)
        search_bar.send_keys(Keys.ENTER)
        msg_bar = browser.find_element(By.XPATH, '/html/body/div[1]/div/div/div[2]/div[4]/div/footer/div[1]/div/span/div/div[2]/div[1]/div/div[1]') # relative xpath of anything that is editable by the user
        msgs = mes.split('\n')
        for m in msgs:
            time.sleep(1)
            msg_bar.send_keys(m)
            time.sleep(1)
            msg_bar.send_keys(Keys.SHIFT + Keys.ENTER) # we press shift + enter so that we can send multi-line texts(\n is used to send a msg in whatsapp)
            msg_bar.send_keys(Keys.SHIFT + Keys.ENTER)
        time.sleep(5)
        msg_bar.send_keys(Keys.ENTER)
        time.sleep(5)
        return 'Scorecard Sent Successfully'
    except Exception as e:
        return 'Error While Sending Scorecard'


send_message('me', msg, browser)


while True:
        time.sleep(300)  # Wait for 5 minutes
        msg = fetch_details(scrap_URL+meow[0])
        time.sleep(5)
