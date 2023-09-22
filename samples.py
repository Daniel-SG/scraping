import random
import re
from urllib.request import urlopen

import requests
from bs4 import BeautifulSoup
from lxml import html

import utils


header = utils.get_header()

# url = "https://www.amazon.es/AmazonBasics-Perchas-terciopelo-trajes-Paquete/dp/B00FXNAAW2"
url = "https://www.marca.com"
# METODO POR ID
# web_content = requests.get(url, headers=header)
# parser = html.fromstring(web_content.text)
# print(web_content.text)
# desc =''
# https://lxml.de/lxmlhtml.html
# description = parser.get_element_by_id("feature-bullets")
# description2 = parser.get_element_by_class("feature-bullets")
# for texto in descripcion.text_content().split('     '):
#    desc += texto

# print(desc)

# METODO POR XPARSER
# web_content = requests.get(url, headers=header)
# parser = html.fromstring(web_content.text)
# pattern_title = f'//*[@id="productTitle"]/text()'
# pattern_title2 = f'//div[contain(@class,'class_name')]//strong/text()'
# title = str(parser.xpath(pattern)[0])

# METODO BEAUTILSOUP
web_content = requests.get(url, headers=header)
soup = BeautifulSoup(web_content.text, "html.parser")
# print title
# print(soup.title.text)
# print all links in a web
# for link in soup.find_all('a'):
    # print(link.get('href'))

