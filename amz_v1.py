import json
import requests
from bs4 import BeautifulSoup
from lxml import html
import utils


def scraping(header, used_links):
    header = ({'User-Agent':
                    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
                'Accept-Language': 'en-US, en;q=0.5'})
    try:
        url = 'https://www.amazon.es/deal/70a6938d'
        web_content = requests.get(url, headers=header)
        soup = BeautifulSoup(web_content.text, "lxml")
        l = soup.select('.a-link-normal')
        print(l[0])

    except Exception:
        print('a')
