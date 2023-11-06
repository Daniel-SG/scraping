import re
import requests
from lxml import html

import send_message
import utils
from blog.insert_blog import format_post


def scraping(header, used_links):
    utils.read_log()
    url = "https://www.ofertitas.es/etiqueta/amazon-espana/"
    web_content = requests.get(url, headers=header)
    parser = html.fromstring(web_content.text)

    i = 1
    while i < 5:
        pattern_title = f'//*[@id="pt-cv-view-50e3eed6kg"]/div/div[{i}]/div/h3/a/text()'
        pattern_link_ofertitas = f'//*[@id="pt-cv-view-50e3eed6kg"]/div/div[{i}]/div/h3/a/@href'
        pattern_price = r'\d{1,3},\d{1,2}€'
        pattern_discount = r'\d{1,2}%'
        if parser.xpath(pattern_title):
            title = str(parser.xpath(pattern_title)[0]).replace('Chollo','').replace('Chollazo','').strip()
            link_ofertitas = str(parser.xpath(pattern_link_ofertitas)[0])
            matches_price = re.findall(pattern_price, title)
            matches_discount = re.findall(pattern_discount, title)

            if matches_price and matches_discount:
                price = matches_price[0]
                price_float = float(price.replace(',', '.')[:-1])
                discount = matches_discount[0]
                discount_int = int(discount[:-1])
                old_price = round(price_float / (1 - discount_int/100),2)

                # Go inside the link and grab the amazon url

                web_content2 = requests.get(link_ofertitas, headers=header)
                parser_specific = html.fromstring(web_content2.text)

                postID = link_ofertitas.split('/')[-2]
                pattern_specific_link = f'//*[@id="post-{postID}"]/div/div/div[1]/p[3]/a/@href'

                specific_link = str(parser_specific.xpath(pattern_specific_link)[0])
                if specific_link.__contains__('www.ofertitas.es'):
                    amazon_ref = specific_link[specific_link.find('=')+1:]
                elif specific_link.__contains__('amazon'):
                    amazon_ref = specific_link.split('?')[0].split('/')[5]
                amazon_url = 'https://www.amazon.es/gp/product/' + amazon_ref

                if not amazon_url in used_links:
                    print(title)
                    print(amazon_url)
                    print('current_price ' + str(price))
                    print('old_price ' + str(old_price))
                    print('discount ' + str(discount) + '\n')
                    # send_message.send_to_whats(amazon_url, price, 0)
                    utils.write_log(amazon_url)
                    format_post(title, price, old_price)
        i = i + 1

# TODO anadir los demas posts, ahora solo muestra los 4 ultimos