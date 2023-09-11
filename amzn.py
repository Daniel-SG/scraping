import json
import requests
from lxml import html
import utils
from bs4 import BeautifulSoup


def get_url(perc, category1, category2):
    # https://meyerweb.com/eric/tools/dencoder/

    url = ''
    if perc == 90:
        url = f'https://www.amazon.es/deals?ref_=nav_cs_gb&deals-widget=%257B%2522version%2522%253A1%252C%2522viewIndex%2522%253A0%252C%2522presetId%2522%253A%2522deals-collection-all-deals%2522%252C%2522discountRanges%2522%253A%255B%250A%257B%2522sectionText%2522%253A%2522Descuento%2522%252C%2522optionText%2522%253A%252210%2525%2520de%2520descuento%2520o%2520m%25C3%25A1s%2522%252C%2522from%2522%253A10%252C%2522to%2522%253Anull%252C%2522selected%2522%253Afalse%257D%252C%250A%257B%2522sectionText%2522%253A%2522Descuento%2522%252C%2522optionText%2522%253A%252220%2525%2520de%2520descuento%2520o%2520m%25C3%25A1s%2522%252C%2522from%2522%253A20%252C%2522to%2522%253Anull%252C%2522selected%2522%253Afalse%257D%252C%250A%257B%2522sectionText%2522%253A%2522Descuento%2522%252C%2522optionText%2522%253A%252230%2525%2520de%2520descuento%2520o%2520m%25C3%25A1s%2522%252C%2522from%2522%253A30%252C%2522to%2522%253Anull%252C%2522selected%2522%253Afalse%257D%252C%250A%257B%2522sectionText%2522%253A%2522Descuento%2522%252C%2522optionText%2522%253A%252290%2525%2520de%2520descuento%2520o%2520m%25C3%25A1s%2522%252C%2522from%2522%253A90%252C%2522to%2522%253Anull%252C%2522selected%2522%253Atrue%257D%250A%255D%252C%2522departments%2522%253A%255B%2522{category1}2522%252C%2522{category2}%2522%255D%252C%2522sorting%2522%253A%2522FEATURED%2522%257D'
    elif perc == 80:
        url = f'https://www.amazon.es/deals?ref_=nav_cs_gb&deals-widget=%257B%2522version%2522%253A1%252C%2522viewIndex%2522%253A0%252C%2522presetId%2522%253A%2522deals-collection-all-deals%2522%252C%2522discountRanges%2522%253A%255B%250A%257B%2522sectionText%2522%253A%2522Descuento%2522%252C%2522optionText%2522%253A%252210%2525%2520de%2520descuento%2520o%2520m%25C3%25A1s%2522%252C%2522from%2522%253A10%252C%2522to%2522%253Anull%252C%2522selected%2522%253Afalse%257D%252C%250A%257B%2522sectionText%2522%253A%2522Descuento%2522%252C%2522optionText%2522%253A%252220%2525%2520de%2520descuento%2520o%2520m%25C3%25A1s%2522%252C%2522from%2522%253A20%252C%2522to%2522%253Anull%252C%2522selected%2522%253Afalse%257D%252C%250A%257B%2522sectionText%2522%253A%2522Descuento%2522%252C%2522optionText%2522%253A%252230%2525%2520de%2520descuento%2520o%2520m%25C3%25A1s%2522%252C%2522from%2522%253A30%252C%2522to%2522%253Anull%252C%2522selected%2522%253Afalse%257D%252C%250A%257B%2522sectionText%2522%253A%2522Descuento%2522%252C%2522optionText%2522%253A%252280%2525%2520de%2520descuento%2520o%2520m%25C3%25A1s%2522%252C%2522from%2522%253A80%252C%2522to%2522%253Anull%252C%2522selected%2522%253Atrue%257D%250A%255D%252C%2522departments%2522%253A%255B%2522{category1}%2522%252C%2522{category2}%2522%255D%252C%2522sorting%2522%253A%2522FEATURED%2522%257D'
    elif perc == 70:
        url = f'https://www.amazon.es/deals?ref_=nav_cs_gb&deals-widget=%257B%2522version%2522%253A1%252C%2522viewIndex%2522%253A0%252C%2522presetId%2522%253A%2522deals-collection-all-deals%2522%252C%2522discountRanges%2522%253A%255B%250A%257B%2522sectionText%2522%253A%2522Descuento%2522%252C%2522optionText%2522%253A%252210%2525%2520de%2520descuento%2520o%2520m%25C3%25A1s%2522%252C%2522from%2522%253A10%252C%2522to%2522%253Anull%252C%2522selected%2522%253Afalse%257D%252C%250A%257B%2522sectionText%2522%253A%2522Descuento%2522%252C%2522optionText%2522%253A%252220%2525%2520de%2520descuento%2520o%2520m%25C3%25A1s%2522%252C%2522from%2522%253A20%252C%2522to%2522%253Anull%252C%2522selected%2522%253Afalse%257D%252C%250A%257B%2522sectionText%2522%253A%2522Descuento%2522%252C%2522optionText%2522%253A%252230%2525%2520de%2520descuento%2520o%2520m%25C3%25A1s%2522%252C%2522from%2522%253A30%252C%2522to%2522%253Anull%252C%2522selected%2522%253Afalse%257D%252C%250A%257B%2522sectionText%2522%253A%2522Descuento%2522%252C%2522optionText%2522%253A%252270%2525%2520de%2520descuento%2520o%2520m%25C3%25A1s%2522%252C%2522from%2522%253A70%252C%2522to%2522%253Anull%252C%2522selected%2522%253Atrue%257D%250A%255D%252C%2522departments%2522%253A%255B%2522{category1}%2522%252C%2522{category2}%2522%255D%252C%2522sorting%2522%253A%2522FEATURED%2522%257D'
    elif perc == 60:
        url = f'https://www.amazon.es/deals?ref_=nav_cs_gb&deals-widget=%257B%2522version%2522%253A1%252C%2522viewIndex%2522%253A0%252C%2522presetId%2522%253A%2522deals-collection-all-deals%2522%252C%2522discountRanges%2522%253A%255B%250A%257B%2522sectionText%2522%253A%2522Descuento%2522%252C%2522optionText%2522%253A%252210%2525%2520de%2520descuento%2520o%2520m%25C3%25A1s%2522%252C%2522from%2522%253A10%252C%2522to%2522%253Anull%252C%2522selected%2522%253Afalse%257D%252C%250A%257B%2522sectionText%2522%253A%2522Descuento%2522%252C%2522optionText%2522%253A%252220%2525%2520de%2520descuento%2520o%2520m%25C3%25A1s%2522%252C%2522from%2522%253A20%252C%2522to%2522%253Anull%252C%2522selected%2522%253Afalse%257D%252C%250A%257B%2522sectionText%2522%253A%2522Descuento%2522%252C%2522optionText%2522%253A%252230%2525%2520de%2520descuento%2520o%2520m%25C3%25A1s%2522%252C%2522from%2522%253A30%252C%2522to%2522%253Anull%252C%2522selected%2522%253Afalse%257D%252C%250A%257B%2522sectionText%2522%253A%2522Descuento%2522%252C%2522optionText%2522%253A%252260%2525%2520de%2520descuento%2520o%2520m%25C3%25A1s%2522%252C%2522from%2522%253A60%252C%2522to%2522%253Anull%252C%2522selected%2522%253Atrue%257D%250A%255D%252C%2522departments%2522%253A%255B%2522{category1}%2522%252C%2522{category2}%2522%255D%252C%2522sorting%2522%253A%2522FEATURED%2522%257D'
    elif perc == 50:
        url = f'https://www.amazon.es/deals?ref_=nav_cs_gb&deals-widget=%257B%2522version%2522%253A1%252C%2522viewIndex%2522%253A0%252C%2522presetId%2522%253A%2522deals-collection-all-deals%2522%252C%2522discountRanges%2522%253A%255B%250A%257B%2522sectionText%2522%253A%2522Descuento%2522%252C%2522optionText%2522%253A%252210%2525%2520de%2520descuento%2520o%2520m%25C3%25A1s%2522%252C%2522from%2522%253A10%252C%2522to%2522%253Anull%252C%2522selected%2522%253Afalse%257D%252C%250A%257B%2522sectionText%2522%253A%2522Descuento%2522%252C%2522optionText%2522%253A%252220%2525%2520de%2520descuento%2520o%2520m%25C3%25A1s%2522%252C%2522from%2522%253A20%252C%2522to%2522%253Anull%252C%2522selected%2522%253Afalse%257D%252C%250A%257B%2522sectionText%2522%253A%2522Descuento%2522%252C%2522optionText%2522%253A%252230%2525%2520de%2520descuento%2520o%2520m%25C3%25A1s%2522%252C%2522from%2522%253A30%252C%2522to%2522%253Anull%252C%2522selected%2522%253Afalse%257D%252C%250A%257B%2522sectionText%2522%253A%2522Descuento%2522%252C%2522optionText%2522%253A%252250%2525%2520de%2520descuento%2520o%2520m%25C3%25A1s%2522%252C%2522from%2522%253A50%252C%2522to%2522%253Anull%252C%2522selected%2522%253Atrue%257D%250A%255D%252C%2522departments%2522%253A%255B%2522{category1}%2522%252C%2522{category2}%2522%255D%252C%2522sorting%2522%253A%2522FEATURED%2522%257D'

    return url


def scraping(header, used_links):
    try:

        category1 = utils.get_amazon_categories()
        category2 = utils.get_amazon_categories()
        category_page_list = []

        starting = False
        discount = 90
        while not starting:
            url = get_url(discount,category1, category2)
            # url = f'https://www.amazon.es/deals?ref_=nav_cs_gb&deals-widget=%257B%2522version%2522%253A1%252C%2522viewIndex%2522%253A0%252C%2522presetId%2522%253A%2522deals-collection-all-deals%2522%252C%2522discountRanges%2522%253A%255B%250A%257B%2522sectionText%2522%253A%2522Descuento%2522%252C%2522optionText%2522%253A%252210%2525%2520de%2520descuento%2520o%2520m%25C3%25A1s%2522%252C%2522from%2522%253A10%252C%2522to%2522%253Anull%252C%2522selected%2522%253Afalse%257D%252C%250A%257B%2522sectionText%2522%253A%2522Descuento%2522%252C%2522optionText%2522%253A%252220%2525%2520de%2520descuento%2520o%2520m%25C3%25A1s%2522%252C%2522from%2522%253A20%252C%2522to%2522%253Anull%252C%2522selected%2522%253Afalse%257D%252C%250A%257B%2522sectionText%2522%253A%2522Descuento%2522%252C%2522optionText%2522%253A%252230%2525%2520de%2520descuento%2520o%2520m%25C3%25A1s%2522%252C%2522from%2522%253A30%252C%2522to%2522%253Anull%252C%2522selected%2522%253Afalse%257D%252C%250A%257B%2522sectionText%2522%253A%2522Descuento%2522%252C%2522optionText%2522%253A%252250%2525%2520de%2520descuento%2520o%2520m%25C3%25A1s%2522%252C%2522from%2522%253A50%252C%2522to%2522%253Anull%252C%2522selected%2522%253Atrue%257D%250A%255D%252C%2522departments%2522%253A%255B%2522{2454136031}%2522%252C%2522{1703495031}%2522%255D%252C%2522sorting%2522%253A%2522FEATURED%2522%257D'
            starting = get_content(url, header)
            discount = discount - 10
            if discount < 50:
                discount = 80
                category1 = utils.get_amazon_categories()
                category2 = utils.get_amazon_categories()

        # Iterate in every category group shown on the web
        for category in starting['entities']:
            if category['entity']['details']['entity']['title']:
                category_title = category['entity']['details']['entity']['title']
                # if category['entity']['badge']['entity']['label']['content']['fragments'][0]['text'] == 'Hasta un -':
                category_discount = category['entity']['badge']['entity']['label']['content']['fragments'][1]['text']
                url = "https://www.amazon.es/deal/" + category['entity']['id']
                category_page_list.append((category_discount, url, category_title))

        sorted_category_page_list = sorted(category_page_list, key=lambda discount: discount[0], reverse=True)

        # Take the 5 groups with most discount
        for category_page in sorted_category_page_list[:5]:
            more_elements = True
            i = 1
            link_group_page = category_page[1]
            web_content_group_page = requests.get(link_group_page, headers=header)
            parser = html.fromstring(web_content_group_page.text)
            most_discount_product = []
            biggest_discount = 0
            while more_elements:
                pattern_title = f"//*[@id='octopus-dlp-asin-stream']/ul/li[{i}]/span/div/div[2]/div[1]/a/text()"
                pattern_url = f"//*[@id='octopus-dlp-asin-stream']/ul/li[{i}]/span/div/div[1]/a/@href"
                pattern_price = f"//*[@id='octopus-dlp-asin-stream']/ul/li[{i}]/span/div/div[2]/div[4]/span[2]/span[1]/text()"
                pattern_old_price = f"//*[@id='octopus-dlp-asin-stream']/ul/li[{i}]/span/div/div[2]/div[4]/span[3]/span[2]/text()"
                pattern_reduction_price = f"//*[@id='octopus-dlp-asin-stream']/ul/li[{i}]/span/div/div[2]/div[4]/span[1]/span/text()"

                if len(parser.xpath(pattern_title)) > 0:
                    title_product = str(parser.xpath(pattern_title)[0]).strip()
                    product_url = str(parser.xpath(pattern_url)[0])
                    amazon_url = 'https://www.amazon.es' + product_url[:product_url.find('?')]
                    final_product_price = str(parser.xpath(pattern_price)[0])
                    final_product_price_float = float(final_product_price[:-2].replace('.', '').replace(',', '.'))
                    reduction_price_str = '-' + str(parser.xpath(pattern_reduction_price)[0])[1:-2] + '%'
                    reduction_price = int(str(parser.xpath(pattern_reduction_price)[0])[1:-2])

                    if len(parser.xpath(pattern_old_price)) > 0:
                        old_price = str(parser.xpath(pattern_old_price)[0]).strip()
                    else:
                        old_price = round((int(final_product_price_float) * 100) / (100 - reduction_price), 2)

                    i = i + 1
                    if amazon_url not in used_links and reduction_price > biggest_discount:
                        biggest_discount = reduction_price
                        most_discount_product = (
                            reduction_price_str, title_product, amazon_url, final_product_price, old_price)

                else:
                    more_elements = False
            if len(most_discount_product) > 0:
                print('title: ' + str(most_discount_product[1]))
                print('url: ' + str(most_discount_product[2]))
                print('current_price ' + str(most_discount_product[3]))
                print('old_price ' + str(most_discount_product[4]))
                print('discount ' + str(most_discount_product[0] + '\n'))
                # send_message.send_to_whats(amazon_url, price, 0)
                utils.write_log(most_discount_product[2])
                
    except Exception as e:
        print(str(e))
        print(amazon_url)
        print('discount' + str(discount))
        print(category1)
        print(category2)


def get_content(url, header):
    web_content = requests.get(url, headers=header)

    # identy start of json with the content
    i = web_content.text.find("{\"widgetId\"")
    partial_res = web_content.text[i:]
    f = partial_res.find('</script>') - 36
    parsed = json.loads(partial_res[:f])
    if (len(parsed['prefetchedData']['aapiGetDealsList'])) > 0:
        starting = parsed['prefetchedData']['aapiGetDealsList'][0]
    else:
        starting = False
    return starting

# soup = BeautifulSoup(web_content.content, 'html.parser')
# print(soup)
# parser = html.fromstring(web_content.text)
#
# pattern_product = "//*[@id='grid-main-container']/div[3]/div/div[1]/div/div/div/span/div[1]/div/text()"
# url_product = str(parser.xpath(pattern_product))
