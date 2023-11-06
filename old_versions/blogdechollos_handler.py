from lxml import html
import requests
import utils


def scraping(header, used_links):
    url = "https://www.blogdechollos.com/"

    web_content = requests.get(url, headers=header)
    parser = html.fromstring(web_content.text)
    date_added = 'Hoy'
    title, old_price, new_price, discount_percentage, image_url, description = '', '', '', '', '', ''
    i = 1

    while date_added.__contains__('Hoy'):
        pattern_product = f"//*[@id='main']/div/div/div[{i}]/div[3]/a/@href"
        url_product = str(parser.xpath(pattern_product))
        pattern_date_added = f'//*[@id="main"]/div/div/div[{i}]/div[4]/div/div/p[1]/text()'
        i = i + 1
        if url_product.__contains__('https://www.amazon.es'):
            amazon_url = url_product[2:url_product.find('?')]
            response = requests.get(amazon_url, headers=header)
            if response.status_code == 200:
                price = str(parser.xpath(pattern_price)[0])
                if len(parser.xpath(pattern_old_price)) > 0 :
                    tmp_title = str(parser.xpath(pattern_title)[0]).\
                        replace('¡¡Chollo!!','').replace('¡Precio mínimo histórico!','')
                    title = tmp_title[:tmp_title.find('.')].strip()
                    old_price = str(parser.xpath(pattern_old_price)[0])
                    discount = str(parser.xpath(pattern_discount)[0])
                    added = str(parser.xpath(pattern_added)[0])
                    if not amazon_url in used_links:
                        print(title)
                        print(amazon_url)
                        print('current_price ' + price)
                        print('old_price ' + old_price)
                        print('discount ' + discount + '\n')
                        utils.write_log(amazon_url)
                    # send_message.send_to_whats(amazon_url,price,old_price)
        i = i + 1

