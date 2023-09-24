import random
import re
from urllib.request import urlopen

import requests
from bs4 import BeautifulSoup
from lxml import html
import webbrowser

from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

import utils



header = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36",
}

# url = "https://www.amazon.es/AmazonBasics-Perchas-terciopelo-trajes-Paquete/dp/B00FXNAAW2"
url = "https://www.amazon.es/JUMPER-Ordenador-port%C3%A1til-Altavoces-Bluetooth/dp/B0CG678KXG"
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
#web_content = requests.get(url, headers=header)
#soup = BeautifulSoup(web_content.text, "lxml")
# print title
#print(soup.select('title')[0].getText())
# soup.select('div') -> all element with 'div' tag
# soup.select('#some_div') element containing id='some_id'
# soup.select('.some_class') elements containing class='some_class'
# soup.select('div span') any elements named span within a div element
# soup.select('div > span') any elements named span directly within a div element with nothing in between
#image = requests.get("image_url")
# print all links in a web
# for link in soup.find_all('a'):
    # print(link.get('href'))

# SELENIUM
from selenium import webdriver

#normal case:
browser = webdriver.Firefox()
#si falla por geock driver, seguir passos:
#https://stackoverflow.com/questions/40208051/selenium-using-python-geckodriver-executable-needs-to-be-in-path

browser.get('http://books.toscrape.com/')
a = browser.find_element_by_css_selector('li.col-xs-6:nth-child(1) > article:nth-child(1) > div:nth-child(4)')
#a.click() #simulates a click on that element
browser.quit()