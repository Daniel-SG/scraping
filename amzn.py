import json

import requests
from lxml import html
from bs4 import BeautifulSoup


url = "https://www.amazon.es/deals?ref_=nav_cs_gb&deals-widget=%257B%2522version%2522%253A1%252C%2522viewIndex%2522%253A0%252C%2522presetId%2522%253A%2522deals-collection-all-deals%2522%252C%2522discountRanges%2522%253A%255B%250A%257B%2522sectionText%2522%253A%2522Descuento%2522%252C%2522optionText%2522%253A%252210%2525%2520de%2520descuento%2520o%2520m%25C3%25A1s%2522%252C%2522from%2522%253A10%252C%2522to%2522%253Anull%252C%2522selected%2522%253Afalse%257D%252C%250A%250A%257B%2522sectionText%2522%253A%2522Descuento%2522%252C%2522optionText%2522%253A%252220%2525%2520de%2520descuento%2520o%2520m%25C3%25A1s%2522%252C%2522from%2522%253A20%252C%2522to%2522%253Anull%252C%2522selected%2522%253Afalse%257D%252C%250A%250A%257B%2522sectionText%2522%253A%2522Descuento%2522%252C%2522optionText%2522%253A%252230%2525%2520de%2520descuento%2520o%2520m%25C3%25A1s%2522%252C%2522from%2522%253A30%252C%2522to%2522%253Anull%252C%2522selected%2522%253Afalse%257D%252C%250A%250A%257B%2522sectionText%2522%253A%2522Descuento%2522%252C%2522optionText%2522%253A%252240%2525%2520de%2520descuento%2520o%2520m%25C3%25A1s%2522%252C%2522from%2522%253A40%252C%2522to%2522%253Anull%252C%2522selected%2522%253Afalse%257D%252C%250A%257B%2522sectionText%2522%253A%2522Descuento%2522%252C%2522optionText%2522%253A%252290%2525%2520de%2520descuento%2520o%2520m%25C3%25A1s%2522%252C%2522from%2522%253A90%252C%2522to%2522%253Anull%252C%2522selected%2522%253Atrue%257D%250A%250A%255D%252C%2522sorting%2522%253A%2522FEATURED%2522%257D"
# url = "https://www.amazon.es/deals?ref_=nav_cs_gb"
url = "https://www.amazon.es/deals?ref_=nav_cs_gb&deals-widget=%257B%2522version%2522%253A1%252C%2522viewIndex%2522%253A0%252C%2522presetId%2522%253A%2522deals-collection-all-deals%2522%252C%2522discountRanges%2522%253A%255B%257B%2522sectionText%2522%253A%2522Descuento%2522%252C%2522optionText%2522%253A%252210%2525%2520de%2520descuento%2520o%2520m%25C3%25A1s%2522%252C%2522from%2522%253A10%252C%2522to%2522%253Anull%252C%2522selected%2522%253Afalse%257D%252C%257B%2522sectionText%2522%253A%2522Descuento%2522%252C%2522optionText%2522%253A%252220%2525%2520de%2520descuento%2520o%2520m%25C3%25A1s%2522%252C%2522from%2522%253A20%252C%2522to%2522%253Anull%252C%2522selected%2522%253Afalse%257D%252C%257B%2522sectionText%2522%253A%2522Descuento%2522%252C%2522optionText%2522%253A%252230%2525%2520de%2520descuento%2520o%2520m%25C3%25A1s%2522%252C%2522from%2522%253A30%252C%2522to%2522%253Anull%252C%2522selected%2522%253Afalse%257D%252C%257B%2522sectionText%2522%253A%2522Descuento%2522%252C%2522optionText%2522%253A%252260%2525%2520de%2520descuento%2520o%2520m%25C3%25A1s%2522%252C%2522from%2522%253A60%252C%2522to%2522%253Anull%252C%2522selected%2522%253Atrue%257D%255D%252C%2522departments%2522%253A%255B%25221703495031%2522%252C%2522599370031%2522%252C%2522667049031%2522%252C%252212472654031%2522%252C%25222822691031%2522%255D%252C%2522sorting%2522%253A%2522FEATURED%2522%252C%2522starRating%2522%253A4%257D"
header = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36",
}

web_content = requests.get(url, headers=header)
# print(web_content.text)

# soup = BeautifulSoup(web_content.content, 'html.parser')
# print(soup)
# parser = html.fromstring(web_content.text)
#
# pattern_product = "//*[@id='grid-main-container']/div[3]/div/div[1]/div/div/div/span/div[1]/div/text()"
# url_product = str(parser.xpath(pattern_product))
i = web_content.text.find("{\"widgetId\"")
partial_res = web_content.text[i:]
f = partial_res.find('</script>') - 36

parsed = json.loads(partial_res[:f])
starting = parsed['prefetchedData']['aapiGetDealsList'][0]

for product in starting['entities']:
    title = product['entity']['details']['entity']['title']
    current_price = product['entity']['details']['entity']['price']['details']['dealPrice']['moneyValueOrRange']['range']['max']['amount']
    offer_type = product['entity']['badge']['entity']['label']['content']['fragments'][1]['text']


    # skip cases where there is no % reduction
    if offer_type.strip() != 'o menos':
        discount =  product['entity']['badge']['entity']['label']['content']['fragments'][1]['text']
        url = product['entity']['id']
        print(discount,title,current_price,offer_type)
