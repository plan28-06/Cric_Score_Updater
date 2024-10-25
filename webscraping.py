import requests # We use requests module to get the HTML structure of the desired URL
from bs4 import BeautifulSoup
from termcolor import colored
URL = "https://www.cricbuzz.com"

def overview():
    resp = requests.get(URL)
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
    for row in table:
        if(row[0]=='Batter' or row[0]=='Bowler'):
            print(colored("{:<24} {:<8} {:<8} {:<8} {:<8} {:<8}".format(row[0], row[1], row[2], row[3], row[4], row[5]), 'cyan', attrs=['bold']))
        else:
            print(colored("{:<24} {:<8} {:<8} {:<8} {:<8} {:<8}".format(row[0], row[1], row[2], row[3], row[4], row[5]), 'white'))

meow = overview()

fetch_details(URL+meow[0])