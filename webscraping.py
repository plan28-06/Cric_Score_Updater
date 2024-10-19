import requests # We use requests module to get the HTML structure of the desired URL
from bs4 import BeautifulSoup
from termcolor import colored

def overview():
    URL = "https://www.cricbuzz.com"
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

