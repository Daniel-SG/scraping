import json

import requests
from lxml import html
from bs4 import BeautifulSoup

import utils


def scraping(header,used_links):
    page_list = []
    url = "https://www.amazon.es/deals?ref_=nav_cs_gb&deals-widget=%257B%2522version%2522%253A1%252C%2522viewIndex%2522%253A0%252C%2522presetId%2522%253A%2522deals-collection-all-deals%2522%252C%2522discountRanges%2522%253A%255B%257B%2522sectionText%2522%253A%2522Descuento%2522%252C%2522optionText%2522%253A%252210%2525%2520de%2520descuento%2520o%2520m%25C3%25A1s%2522%252C%2522from%2522%253A10%252C%2522to%2522%253Anull%252C%2522selected%2522%253Afalse%257D%252C%257B%2522sectionText%2522%253A%2522Descuento%2522%252C%2522optionText%2522%253A%252220%2525%2520de%2520descuento%2520o%2520m%25C3%25A1s%2522%252C%2522from%2522%253A20%252C%2522to%2522%253Anull%252C%2522selected%2522%253Afalse%257D%252C%257B%2522sectionText%2522%253A%2522Descuento%2522%252C%2522optionText%2522%253A%252230%2525%2520de%2520descuento%2520o%2520m%25C3%25A1s%2522%252C%2522from%2522%253A30%252C%2522to%2522%253Anull%252C%2522selected%2522%253Afalse%257D%252C%257B%2522sectionText%2522%253A%2522Descuento%2522%252C%2522optionText%2522%253A%252260%2525%2520de%2520descuento%2520o%2520m%25C3%25A1s%2522%252C%2522from%2522%253A60%252C%2522to%2522%253Anull%252C%2522selected%2522%253Atrue%257D%255D%252C%2522departments%2522%253A%255B%25221703495031%2522%252C%2522599370031%2522%252C%2522667049031%2522%252C%252212472654031%2522%252C%25222822691031%2522%255D%252C%2522sorting%2522%253A%2522FEATURED%2522%252C%2522starRating%2522%253A4%257D"
    web_content = requests.get(url, headers=header)
    # print(web_content.text)

    # identy start of json with the content
    i = web_content.text.find("{\"widgetId\"")
    partial_res = web_content.text[i:]
    f = partial_res.find('</script>') - 36
    parsed = json.loads(partial_res[:f])
    starting = parsed['prefetchedData']['aapiGetDealsList'][0]

    # Iterate in every product group shown on the web
    for product in starting['entities']:
        title = product['entity']['details']['entity']['title']
        if product['entity']['badge']['entity']['label']['content']['fragments'][0]['text'] == 'Hasta un -':
            discount = product['entity']['badge']['entity']['label']['content']['fragments'][1]['text']
        url = "https://www.amazon.es/deal/" + product['entity']['id']
        # offer_type = product['entity']['badge']['entity']['label']['content']['fragments'][1]['text']
        # current_price = product['entity']['details']['entity']['price']['details']['dealPrice']['moneyValueOrRange']['range']['max']['amount']

        # skip cases where there is no % reduction
        # if offer_type.strip() != 'o menos':
            #
        page_list.append((discount,url,title))
    sorted_page_list = sorted(page_list, key=lambda discount: discount[0],reverse=True)

    for prod_page in sorted_page_list[:4]:
        more_elements = True
        i = 1
        link_prod_page = prod_page[1]
        web_content_prod_page = requests.get(link_prod_page, headers=header)
        parser = html.fromstring(web_content_prod_page.text)

        while more_elements:
            pattern_title = f"//*[@id='octopus-dlp-asin-stream']/ul/li[{i}]/span/div/div[2]/div[1]/a/text()"
            pattern_url = f"//*[@id='octopus-dlp-asin-stream']/ul/li[{i}]/span/div/div[1]/a/@href"
            pattern_price = f"//*[@id='octopus-dlp-asin-stream']/ul/li[{i}]/span/div/div[2]/div[4]/span[1]/span[1]/text()"
            pattern_old_price = f"///*[@id='octopus-dlp-asin-stream']/ul/li[{i}]/span/div/div[2]/div[4]/span[2]/span[2]/text()"
            pattern_reduction_price = f"//*[@id='octopus-dlp-asin-stream']/ul/li[{i}]/span/div/div[2]/div[3]/div/div[1]/span[2]/text()"

            if len(parser.xpath(pattern_title)) > 0:
                title_product = str(parser.xpath(pattern_title)[0]).strip()
                product_url = str(parser.xpath(pattern_url)[0])
                final_product_url = 'https://www.amazon.es'+product_url[:product_url.find('?')]
                final_product_price = str(parser.xpath(pattern_price)[0])
                old_price = str(parser.xpath(pattern_old_price)[0]).strip()
                reduction_price = '-' + str(parser.xpath(pattern_reduction_price)[0]).strip()+'%'

                i = i + 1
                if not final_product_url in used_links:
                    print(title, final_product_price, reduction_price, final_product_url)
                    # send_message.send_to_whats(amazon_url, price, 0)
                    utils.write_log(final_product_url)
            else:
                more_elements = False


# soup = BeautifulSoup(web_content.content, 'html.parser')
# print(soup)
# parser = html.fromstring(web_content.text)
#
# pattern_product = "//*[@id='grid-main-container']/div[3]/div/div[1]/div/div/div/span/div[1]/div/text()"
# url_product = str(parser.xpath(pattern_product))
