import json
import requests
from lxml import html

import amz_v1
import utils
from bs4 import BeautifulSoup

from amzn_selenium import amazn_scrap_selenium
from blog.insert_blog import format_post


def get_url(category1, category2=None):
    # https://meyerweb.com/eric/tools/dencoder/

    url = ''
    # if perc == 90:
    #     url = f'https://www.amazon.es/deals?ref_=nav_cs_gb&deals-widget=%257B%2522version%2522%253A1%252C%2522viewIndex%2522%253A0%252C%2522presetId%2522%253A%2522deals-collection-all-deals%2522%252C%2522discountRanges%2522%253A%255B%250A%257B%2522sectionText%2522%253A%2522Descuento%2522%252C%2522optionText%2522%253A%252210%2525%2520de%2520descuento%2520o%2520m%25C3%25A1s%2522%252C%2522from%2522%253A10%252C%2522to%2522%253Anull%252C%2522selected%2522%253Afalse%257D%252C%250A%257B%2522sectionText%2522%253A%2522Descuento%2522%252C%2522optionText%2522%253A%252220%2525%2520de%2520descuento%2520o%2520m%25C3%25A1s%2522%252C%2522from%2522%253A20%252C%2522to%2522%253Anull%252C%2522selected%2522%253Afalse%257D%252C%250A%257B%2522sectionText%2522%253A%2522Descuento%2522%252C%2522optionText%2522%253A%252230%2525%2520de%2520descuento%2520o%2520m%25C3%25A1s%2522%252C%2522from%2522%253A30%252C%2522to%2522%253Anull%252C%2522selected%2522%253Afalse%257D%252C%250A%257B%2522sectionText%2522%253A%2522Descuento%2522%252C%2522optionText%2522%253A%252290%2525%2520de%2520descuento%2520o%2520m%25C3%25A1s%2522%252C%2522from%2522%253A90%252C%2522to%2522%253Anull%252C%2522selected%2522%253Atrue%257D%250A%255D%252C%2522departments%2522%253A%255B%2522{category1}2522%252C%2522{category2}%2522%255D%252C%2522sorting%2522%253A%2522FEATURED%2522%257D'
    # elif perc == 80:
    #     url = f'https://www.amazon.es/deals?ref_=nav_cs_gb&deals-widget=%257B%2522version%2522%253A1%252C%2522viewIndex%2522%253A0%252C%2522presetId%2522%253A%2522deals-collection-all-deals%2522%252C%2522discountRanges%2522%253A%255B%250A%257B%2522sectionText%2522%253A%2522Descuento%2522%252C%2522optionText%2522%253A%252210%2525%2520de%2520descuento%2520o%2520m%25C3%25A1s%2522%252C%2522from%2522%253A10%252C%2522to%2522%253Anull%252C%2522selected%2522%253Afalse%257D%252C%250A%257B%2522sectionText%2522%253A%2522Descuento%2522%252C%2522optionText%2522%253A%252220%2525%2520de%2520descuento%2520o%2520m%25C3%25A1s%2522%252C%2522from%2522%253A20%252C%2522to%2522%253Anull%252C%2522selected%2522%253Afalse%257D%252C%250A%257B%2522sectionText%2522%253A%2522Descuento%2522%252C%2522optionText%2522%253A%252230%2525%2520de%2520descuento%2520o%2520m%25C3%25A1s%2522%252C%2522from%2522%253A30%252C%2522to%2522%253Anull%252C%2522selected%2522%253Afalse%257D%252C%250A%257B%2522sectionText%2522%253A%2522Descuento%2522%252C%2522optionText%2522%253A%252280%2525%2520de%2520descuento%2520o%2520m%25C3%25A1s%2522%252C%2522from%2522%253A80%252C%2522to%2522%253Anull%252C%2522selected%2522%253Atrue%257D%250A%255D%252C%2522departments%2522%253A%255B%2522{category1}%2522%252C%2522{category2}%2522%255D%252C%2522sorting%2522%253A%2522FEATURED%2522%257D'
    # elif perc == 70:
    #     url = f'https://www.amazon.es/deals?ref_=nav_cs_gb&deals-widget=%257B%2522version%2522%253A1%252C%2522viewIndex%2522%253A0%252C%2522presetId%2522%253A%2522deals-collection-all-deals%2522%252C%2522discountRanges%2522%253A%255B%250A%257B%2522sectionText%2522%253A%2522Descuento%2522%252C%2522optionText%2522%253A%252210%2525%2520de%2520descuento%2520o%2520m%25C3%25A1s%2522%252C%2522from%2522%253A10%252C%2522to%2522%253Anull%252C%2522selected%2522%253Afalse%257D%252C%250A%257B%2522sectionText%2522%253A%2522Descuento%2522%252C%2522optionText%2522%253A%252220%2525%2520de%2520descuento%2520o%2520m%25C3%25A1s%2522%252C%2522from%2522%253A20%252C%2522to%2522%253Anull%252C%2522selected%2522%253Afalse%257D%252C%250A%257B%2522sectionText%2522%253A%2522Descuento%2522%252C%2522optionText%2522%253A%252230%2525%2520de%2520descuento%2520o%2520m%25C3%25A1s%2522%252C%2522from%2522%253A30%252C%2522to%2522%253Anull%252C%2522selected%2522%253Afalse%257D%252C%250A%257B%2522sectionText%2522%253A%2522Descuento%2522%252C%2522optionText%2522%253A%252270%2525%2520de%2520descuento%2520o%2520m%25C3%25A1s%2522%252C%2522from%2522%253A70%252C%2522to%2522%253Anull%252C%2522selected%2522%253Atrue%257D%250A%255D%252C%2522departments%2522%253A%255B%2522{category1}%2522%252C%2522{category2}%2522%255D%252C%2522sorting%2522%253A%2522FEATURED%2522%257D'
    # elif perc == 60:
    #     url = f'https://www.amazon.es/deals?ref_=nav_cs_gb&deals-widget=%257B%2522version%2522%253A1%252C%2522viewIndex%2522%253A0%252C%2522presetId%2522%253A%2522deals-collection-all-deals%2522%252C%2522discountRanges%2522%253A%255B%250A%257B%2522sectionText%2522%253A%2522Descuento%2522%252C%2522optionText%2522%253A%252210%2525%2520de%2520descuento%2520o%2520m%25C3%25A1s%2522%252C%2522from%2522%253A10%252C%2522to%2522%253Anull%252C%2522selected%2522%253Afalse%257D%252C%250A%257B%2522sectionText%2522%253A%2522Descuento%2522%252C%2522optionText%2522%253A%252220%2525%2520de%2520descuento%2520o%2520m%25C3%25A1s%2522%252C%2522from%2522%253A20%252C%2522to%2522%253Anull%252C%2522selected%2522%253Afalse%257D%252C%250A%257B%2522sectionText%2522%253A%2522Descuento%2522%252C%2522optionText%2522%253A%252230%2525%2520de%2520descuento%2520o%2520m%25C3%25A1s%2522%252C%2522from%2522%253A30%252C%2522to%2522%253Anull%252C%2522selected%2522%253Afalse%257D%252C%250A%257B%2522sectionText%2522%253A%2522Descuento%2522%252C%2522optionText%2522%253A%252260%2525%2520de%2520descuento%2520o%2520m%25C3%25A1s%2522%252C%2522from%2522%253A60%252C%2522to%2522%253Anull%252C%2522selected%2522%253Atrue%257D%250A%255D%252C%2522departments%2522%253A%255B%2522{category1}%2522%252C%2522{category2}%2522%255D%252C%2522sorting%2522%253A%2522FEATURED%2522%257D'
    # elif perc == 50:
    #     url = f'https://www.amazon.es/deals?ref_=nav_cs_gb&deals-widget=%257B%2522version%2522%253A1%252C%2522viewIndex%2522%253A0%252C%2522presetId%2522%253A%2522deals-collection-all-deals%2522%252C%2522discountRanges%2522%253A%255B%250A%257B%2522sectionText%2522%253A%2522Descuento%2522%252C%2522optionText%2522%253A%252210%2525%2520de%2520descuento%2520o%2520m%25C3%25A1s%2522%252C%2522from%2522%253A10%252C%2522to%2522%253Anull%252C%2522selected%2522%253Afalse%257D%252C%250A%257B%2522sectionText%2522%253A%2522Descuento%2522%252C%2522optionText%2522%253A%252220%2525%2520de%2520descuento%2520o%2520m%25C3%25A1s%2522%252C%2522from%2522%253A20%252C%2522to%2522%253Anull%252C%2522selected%2522%253Afalse%257D%252C%250A%257B%2522sectionText%2522%253A%2522Descuento%2522%252C%2522optionText%2522%253A%252230%2525%2520de%2520descuento%2520o%2520m%25C3%25A1s%2522%252C%2522from%2522%253A30%252C%2522to%2522%253Anull%252C%2522selected%2522%253Afalse%257D%252C%250A%257B%2522sectionText%2522%253A%2522Descuento%2522%252C%2522optionText%2522%253A%252250%2525%2520de%2520descuento%2520o%2520m%25C3%25A1s%2522%252C%2522from%2522%253A50%252C%2522to%2522%253Anull%252C%2522selected%2522%253Atrue%257D%250A%255D%252C%2522departments%2522%253A%255B%2522{category1}%2522%252C%2522{category2}%2522%255D%252C%2522sorting%2522%253A%2522FEATURED%2522%257D'

    url = f'https://www.amazon.es/deals?ref_=nav_cs_gb&deals-widget=%257B%2522version%2522%253A1%252C%2522viewIndex%2522%253A0%252C%2522presetId%2522%253A%2522deals-collection-all-deals%2522%252C%2522discountRanges%2522%253A%255B%257B%2522sectionText%2522%253A%2522Descuento%2522%252C%2522optionText%2522%253A%252210%2525%2520de%2520descuento%2520o%2520m%25C3%25A1s%2522%252C%2522from%2522%253A10%252C%2522to%2522%253Anull%252C%2522selected%2522%253Afalse%257D%252C%257B%2522sectionText%2522%253A%2522Descuento%2522%252C%2522optionText%2522%253A%252220%2525%2520de%2520descuento%2520o%2520m%25C3%25A1s%2522%252C%2522from%2522%253A20%252C%2522to%2522%253Anull%252C%2522selected%2522%253Afalse%257D%252C%257B%2522sectionText%2522%253A%2522Descuento%2522%252C%2522optionText%2522%253A%252230%2525%2520de%2520descuento%2520o%2520m%25C3%25A1s%2522%252C%2522from%2522%253A30%252C%2522to%2522%253Anull%252C%2522selected%2522%253Afalse%257D%252C%257B%2522sectionText%2522%253A%2522Descuento%2522%252C%2522optionText%2522%253A%252240%2525%2520de%2520descuento%2520o%2520m%25C3%25A1s%2522%252C%2522from%2522%253A40%252C%2522to%2522%253Anull%252C%2522selected%2522%253Atrue%257D%255D%252C%2522departments%2522%253A%255B%2522{category1}%2522%255D%252C%2522dealState%2522%253A%2522AVAILABLE%2522%252C%2522sorting%2522%253A%2522BY_DISCOUNT_DESCENDING%2522%257D'
    return url


def scraping(used_links):
    try:

        category1 = utils.get_amazon_categories()
       # category2 = utils.get_amazon_categories()
        category_page_list = []

        starting = False

        while not starting:
            url = get_url(category1)
            #url = f'https://www.amazon.es/deals?ref_=nav_cs_gb&deals-widget=%257B%2522version%2522%253A1%252C%2522viewIndex%2522%253A0%252C%2522presetId%2522%253A%2522deals-collection-all-deals%2522%252C%2522discountRanges%2522%253A%255B%250A%257B%2522sectionText%2522%253A%2522Descuento%2522%252C%2522optionText%2522%253A%252210%2525%2520de%2520descuento%2520o%2520m%25C3%25A1s%2522%252C%2522from%2522%253A10%252C%2522to%2522%253Anull%252C%2522selected%2522%253Afalse%257D%252C%250A%257B%2522sectionText%2522%253A%2522Descuento%2522%252C%2522optionText%2522%253A%252220%2525%2520de%2520descuento%2520o%2520m%25C3%25A1s%2522%252C%2522from%2522%253A20%252C%2522to%2522%253Anull%252C%2522selected%2522%253Afalse%257D%252C%250A%257B%2522sectionText%2522%253A%2522Descuento%2522%252C%2522optionText%2522%253A%252230%2525%2520de%2520descuento%2520o%2520m%25C3%25A1s%2522%252C%2522from%2522%253A30%252C%2522to%2522%253Anull%252C%2522selected%2522%253Afalse%257D%252C%250A%257B%2522sectionText%2522%253A%2522Descuento%2522%252C%2522optionText%2522%253A%252250%2525%2520de%2520descuento%2520o%2520m%25C3%25A1s%2522%252C%2522from%2522%253A50%252C%2522to%2522%253Anull%252C%2522selected%2522%253Atrue%257D%250A%255D%252C%2522departments%2522%253A%255B%2522{1703495031}%2522%252C%2522{6198055031}%2522%255D%252C%2522sorting%2522%253A%2522FEATURED%2522%257D'
            #url = 'https://www.amazon.es/deal/bd1b5e08'
            # header = utils.get_header()
            starting = get_content(url)
            category1 = utils.get_amazon_categories()
            # category2 = utils.get_amazon_categories()

        # Iterate in every category group shown on the web
        for category in starting['entities']:
            if category['entity']['details']['entity']['title']:
                category_title = category['entity']['details']['entity']['title']
                # if category['entity']['badge']['entity']['label']['content']['fragments'][0]['text'] == 'Hasta un -':
                category_discount = category['entity']['badge']['entity']['label']['content']['fragments'][1]['text']
                url = "https://www.amazon.es/deal/" + category['entity']['id']
                category_page_list.append((category_discount, url, category_title))

        sorted_category_page_list = sorted(category_page_list, key=lambda discount: discount[0], reverse=True)

        # Take groups with the most discount
        for category_page in sorted_category_page_list[:2]:
            link_group_page = category_page[1]
            print(link_group_page)
            precio_actual, precio_anterior, descuento, descripcion, foto_url, title, url = amazn_scrap_selenium(link_group_page)

            # send_message.send_to_whats(amazon_url, price, 0)
            if url not in used_links:
                utils.write_log(url)
                format_post(title, precio_actual, precio_anterior, descuento, foto_url, descripcion, url)
                break
            else:
                pass

    except Exception as e:
        print(str(e))
        # webpage = requests.get(amazon_url, headers=header)
        # soup = BeautifulSoup(webpage.content, "lxml")
        # print('new title: '+soup_get_title(soup))
        # print('new price:'+ utils.get_new_price(parser))
        print('url ' + str(url))
        print(category1)



def get_content(url):
    starting = False
    web_content = requests.get(url)
    # print(web_content.text)
    # identy start of json with the content
    i = web_content.text.find("{\"widgetId\"")
    if i != -1:
        partial_res = web_content.text[i:]
        f = partial_res.find('</script>') - 36
        parsed = json.loads(partial_res[:f])
        if (len(parsed['prefetchedData']['aapiGetDealsList'])) > 0:
            starting = parsed['prefetchedData']['aapiGetDealsList'][0]

    return starting
