import csv
import random
from datetime import date
from lxml import html

import requests

# 'Alimentacion_bebidas' 6198072031
# Limpieza 2165679031
# Audio y video portatil
# Auriculares equipo de audio
# Bebe 1703495031
# Belleza 6198055031
# Bricolaje 2454133031
# CD y vinilos 599373031
# Cerveza 6347711031
# Climatizacion 3605952031
# Coche y moto 1951051031
# Comunicacion 6348071031
# Limpieza 665492031
# Deportes 2454136031
# Dispositivos amazon 599370031
# Electronica 827230031
# Equipaje 599391031
# Fotografia 4772050031
# Grandes electrodomesticos 664660031
# Hogar y cocina 12710835031

categories = {1: 6198072031, 2: 2165679031, 3: 665477031, 4: 934056031, 5: 1703495031, 6: 6198055031, 7: 2454133031,
              8: 599373031,
              9: 6347711031, 10: 3605952031, 11: 1951051031, 12: 6348071031, 13: 665492031, 14: 2454136031,
              15: 599370031,
              16: 827230031, 17: 599391031, 18: 4772050031, 19: 664660031, 20: 12710835031}

header = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36",
}


def write_log(entry):
    if entry:
        f = open("log.csv", "a")
        f.write(entry + ',' + str(date.today()) + "\n")
        f.close()


def read_log():
    used = []
    with open('log.csv', newline='') as csvfile:
        log_list = csv.reader(csvfile, delimiter=',')
        for row in log_list:
            if row:
                used.append(row[0])
    return used


def get_amazon_categories():
    num = random.randrange(1, len(categories))
    return categories[num]


def get_data_product(amazon_url, header):
    web_content = requests.get(amazon_url, headers=header)
    parser = html.fromstring(web_content.text)
    title = get_title(parser)
    old_price = get_old_price(parser)
    new_price = get_new_price(parser)
    discount_percentage = get_discount_percentage(parser)
    image_url = get_image(parser)
    description = get_description(parser)

    return title, old_price, new_price, discount_percentage, image_url, description


def get_description(parser):
    desc = ''
    description = parser.get_element_by_id("feature-bullets")
    for texto in description.text_content().split('     '):
        desc += texto

    desc = desc.replace('Ver más detalles', '')

    return desc


def get_title(parser):
    pattern = '//*[@id="productTitle"]/text()'
    title = str(parser.xpath(pattern)[0])

    return title


def get_old_price(parser):
    pattern = '//*[@id="corePriceDisplay_desktop_feature_div"]/div[2]/span/span[1]/span[2]/span/span[2]/text()'
    old_price = str(parser.xpath(pattern)[0])

    return old_price


def get_new_price(parser):
    pattern_price_int = '//*[@id="corePriceDisplay_desktop_feature_div"]/div[1]/span[3]/span[2]/span[1]/text()'
    pattern_price_decimal = '//*[@id="corePriceDisplay_desktop_feature_div"]/div[1]/span[3]/span[2]/span[2]/text()'
    price_int = str(parser.xpath(pattern_price_int)[0])
    price_decimal = str(parser.xpath(pattern_price_decimal)[0])

    return price_int + ',' + price_decimal + '€'


def get_discount_percentage(parser):
    pattern_percentage = '//*[@id="corePriceDisplay_desktop_feature_div"]/div[1]/span[2]/text()'
    percentage_discount = str(parser.xpath(pattern_percentage)[0])

    return percentage_discount


def get_image(parser):
    pattern_image = '//*[@id="landingImage"]/@src'
    image_url = str(parser.xpath(pattern_image)[0])

    return image_url
