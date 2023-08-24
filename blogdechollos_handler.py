import requests
from lxml import html

import send_message


def scraping(header):
    url = "https://www.blogdechollos.com/"

    web_content = requests.get(url, headers=header)
    parser = html.fromstring(web_content.text)
    added = ''
    i = 1

    while not added.__contains__('Ayer'):
        pattern_product = f"//*[@id='main']/div/div/div[{i}]/div[3]/a/@href"
        url_product = str(parser.xpath(pattern_product))
        pattern_price = f'//*[@id="main"]/div/div/div[{i}]/div[3]/div[2]/div[1]/text()'
        pattern_old_price = f'//*[@id="main"]/div/div/div[{i}]/div[3]/div[2]/div[2]/div[1]/text()'
        pattern_added = f'//*[@id="main"]/div/div/div[{i}]/div[4]/div/div/p[1]/text()'

        if url_product.__contains__('https://www.amazon.es'):
            amazon_url = url_product[2:url_product.find('?')]
            response = requests.get(amazon_url, headers=header)
            if response.status_code == 200:
                price = str(parser.xpath(pattern_price)[0])
                old_price = str(parser.xpath(pattern_old_price)[0])
                added = str(parser.xpath(pattern_added)[0])
                print(amazon_url)
                print('current_price ' + price)
                print('old_price ' + old_price)
                print(added)
                send_message.send_to_whats(amazon_url,price,old_price)
        i = i + 1
        
blogdechollos_handler.py
