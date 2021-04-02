import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import csv

URL = 'https://domik-mo.ru/'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 YaBrowser/20.12.3.140 Yowser/2.5 Safari/537.36',
    'accept': '*/*'}
FILE = 'f_9496061cd41ed70b'


def get_html(url, params=None):
    full_page = requests.get(url, headers=HEADERS, params=params)
    return full_page.text

def get_letters_hrefs():
    html = get_html(URL)
    soup = BeautifulSoup(html, 'html.parser')
    streets = soup.find('div', class_='item-list')
    letters = streets.find_all('a')
    hrefs = []
    for l in letters:
        hrefs.append(URL + l['href'])
    return hrefs


def get_streets_hrefs():
    letter_hrefs = get_letters_hrefs()
    streets_hrefs = []
    for l in letter_hrefs:
        html = get_html(l)
        soup = BeautifulSoup(html, 'html.parser')
        card = soup.find_all('div', class_='item-list')[1]
        streets = card.find_all('a')
        for s in streets:
            streets_hrefs.append(URL + s['href'])

    return streets_hrefs


def get_houses_hrefs():
    streets_hrefs = get_streets_hrefs()
    houses_hrefs = []
    for s in streets_hrefs:
        html = get_html(s)
        soup = BeautifulSoup(html, 'html.parser')
        try:
            card = soup.find_all('div', class_='view-content')
            if len(card) == 2:
                card = card[1]
            else:
                card = None
        except Exception:
            card = soup.find_all('div', class_='item-list')
            if len(card) == 2:
                card = card[1]
            else:
                card = None
        if card is not None:
            houses = card.find_all('a')
            for h in houses:
                houses_hrefs.append(URL + h['href'])
                print(URL+h['href'])

    return houses_hrefs

def parse():
    get_houses_hrefs()




parse()
