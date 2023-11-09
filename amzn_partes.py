import pprint

import utils
from amazon_scraper import AmazonScraper

from blog.insert_blog import format_post


def get_url(category1):
    # https://meyerweb.com/eric/tools/dencoder/

    url = f'https://www.amazon.es/deals?ref_=nav_cs_gb&deals-widget=%257B%2522version%2522%253A1%252C%2522viewIndex%2522%253A0%252C%2522presetId%2522%253A%2522deals-collection-all-deals%2522%252C%2522discountRanges%2522%253A%255B%257B%2522sectionText%2522%253A%2522Descuento%2522%252C%2522optionText%2522%253A%252210%2525%2520de%2520descuento%2520o%2520m%25C3%25A1s%2522%252C%2522from%2522%253A10%252C%2522to%2522%253Anull%252C%2522selected%2522%253Afalse%257D%252C%257B%2522sectionText%2522%253A%2522Descuento%2522%252C%2522optionText%2522%253A%252220%2525%2520de%2520descuento%2520o%2520m%25C3%25A1s%2522%252C%2522from%2522%253A20%252C%2522to%2522%253Anull%252C%2522selected%2522%253Afalse%257D%252C%257B%2522sectionText%2522%253A%2522Descuento%2522%252C%2522optionText%2522%253A%252230%2525%2520de%2520descuento%2520o%2520m%25C3%25A1s%2522%252C%2522from%2522%253A30%252C%2522to%2522%253Anull%252C%2522selected%2522%253Afalse%257D%252C%257B%2522sectionText%2522%253A%2522Descuento%2522%252C%2522optionText%2522%253A%252240%2525%2520de%2520descuento%2520o%2520m%25C3%25A1s%2522%252C%2522from%2522%253A40%252C%2522to%2522%253Anull%252C%2522selected%2522%253Atrue%257D%255D%252C%2522departments%2522%253A%255B%2522{category1}%2522%255D%252C%2522dealState%2522%253A%2522AVAILABLE%2522%252C%2522sorting%2522%253A%2522BY_DISCOUNT_DESCENDING%2522%257D'
    return url


def scraping(used_links):
    try:

        num, name = utils.get_amazon_categories()
        url = get_url(num)
        print(f'Looking for the best offers in: {name}')

        amazon_scraper = AmazonScraper(url, is_headless=True, browser='chrome', output_file='test.json')

        data = amazon_scraper.run()

        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(data)

        # send_message.send_to_whats(amazon_url, price, 0)
        if url not in used_links:
            utils.write_log(url)
            format_post(data['title'], data['discouted_price'], data['original_price'], data['discount'], data['image_url'], data['description'], data['detail_url'])

        else:
            pass

    except Exception as e:
        print(str(e))
        print('url ' + str(url))
        print(category1)




