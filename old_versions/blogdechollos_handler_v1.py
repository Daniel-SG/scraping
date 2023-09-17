import requests
from lxml import html
from urllib.request import urlopen

import requests
from bs4 import BeautifulSoup
import send_message
import utils


def scraping(header,used_links):
    url = "https://www.blogdechollos.com/"

    web_content = requests.get(url, headers=header)
    parser = html.fromstring(web_content.text)
    added = 'Hoy'
    i = 1

    while added.__contains__('Hoy'):
        pattern_product = f"//*[@id='main']/div/div/div[{i}]/div[3]/a/@href"
        url_product = str(parser.xpath(pattern_product))
        pattern_price = f'//*[@id="main"]/div/div/div[{i}]/div[3]/div[2]/div[1]/text()'
        pattern_old_price = f'//*[@id="main"]/div/div/div[{i}]/div[3]/div[2]/div[2]/div[1]/text()'
        pattern_added = f'//*[@id="main"]/div/div/div[{i}]/div[4]/div/div/p[1]/text()'
        pattern_discount = f'//*[@id="main"]/div/div/div[{i}]/div[3]/div[2]/div[2]/div[2]/text()'
        pattern_title = f'//*[@id="main"]/div/div/div[{i}]/div[2]/div/h2/a/text()'
        pattern_picture = f'//*[@id="main"]/div/div/div[{i}]/div[3]/div[1]/a/picture/source/@data-lazy-srcset'


        if url_product.__contains__('https://www.amazon.es'):
            amazon_url = url_product[2:url_product.find('?')]
            response = requests.get(amazon_url, headers=header)
            if response.status_code == 200:
                price = str(parser.xpath(pattern_price)[0])+'€'
                if len(parser.xpath(pattern_old_price)) > 0:
                    tmp_title = str(parser.xpath(pattern_title)[0]).\
                        replace('¡¡Chollo!!', '').replace('¡Precio mínimo histórico!','')
                    title = tmp_title[:tmp_title.find('.')].strip()
                    old_price = str(parser.xpath(pattern_old_price)[0])
                    discount = str(parser.xpath(pattern_discount)[0])
                    added = str(parser.xpath(pattern_added)[0])
                    pic = str(parser.xpath(pattern_picture)[0])

                    if not amazon_url in used_links:
                        pattern_description = f'//*[@id="feature-bullets"]/text()'
                        web_content = requests.get(amazon_url, headers=header)
                        parser = html.fromstring(web_content.text)
                        description = str(parser.xpath(pattern_description)[0])
                        print(description)
                        print(title)
                        print(amazon_url)
                        print(pic)
                        print('current_price ' + price)
                        print('old_price ' + old_price)
                        print('discount ' + discount + '\n')
                        utils.write_log(amazon_url)
                    # send_message.send_to_whats(amazon_url, price, old_price, discount)
        i = i + 1

