import json
import requests
from bs4 import BeautifulSoup
from lxml import html
from operator import itemgetter


def scraping(header, used_links):
    header = ({'User-Agent':
                    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
                'Accept-Language': 'en-US, en;q=0.5'})
    try:
        lista_ofertas = []
        url = 'https://www.amazon.es/deal/70a6938d'
        url = 'https://www.amazon.es/deal/00ba4988'
        web_content = requests.get(url, headers=header)
        # f = open("deal70a6938d.txt", "r", encoding="utf-8")
        #soup = BeautifulSoup(f.read(), "lxml")
        soup = BeautifulSoup(web_content.text, "lxml")

        print(soup)

        elements = soup.find_all("div", attrs={"class":'a-section octopus-dlp-asin-section'})

        for elem in elements:
            titulo = elem.find("a", attrs={"class": 'a-size-base a-color-base a-link-normal a-text-normal'}).string.strip()
            descuento = elem.find("span", attrs={"class": 'a-size-medium a-color-price octopus-widget-saving-percentage'}).string.strip()
            descuento_orden = str(descuento).replace('%', '').replace('-', '').strip()
            precio = elem.find("span", attrs={"class": 'a-offscreen'}).string.strip()
            precio_anterior = elem.find("span", attrs={"class": 'a-size-mini a-color-tertiary octopus-widget-strike-through-price a-text-strike'}).string.strip()
            url = 'https://www.amazon.es'+\
                  elem.find("a", attrs={"class": "a-size-base a-color-base a-link-normal a-text-normal"})['href']
            lista_ofertas.append((descuento_orden, descuento, precio, titulo, url, precio_anterior))
            print(descuento,titulo)
        lista_ofertas = sorted(lista_ofertas, key=itemgetter(0), reverse=True)

        for l in lista_ofertas[:3]:
            print(l)
    except Exception as e:
        print(e)
