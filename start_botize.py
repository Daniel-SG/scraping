import json
import requests
from datetime import datetime, timedelta, date

import utils_botize

header = ({'User-Agent':
               'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 '
               'Safari/537.36',
           'Accept-Language': 'en-US, en;q=0.5'})


def get_last_urls():
    # Cargamos las URLs de los ultimos 7 dias para evitar cargar repetidos

    current_date = datetime.now()
    new_date = current_date - timedelta(days=7)

    query = f"""
        SELECT 
            url
        FROM productos 
        WHERE fecha_publicacion > '{new_date}' 
    
        """
    result = utils_botize.connectDB(query, 'r')

    ultimas_urls = [r[0] for r in result]

    return ultimas_urls


def get_content(header):
    anteriores_url_anadidas = get_last_urls()

    for cat in utils_botize.categories.items():
        cnt_products_per_cat = 0
        cat_id = cat[0]
        cat_name = cat[1]
        print(cat_name)
        print('\t')
        url = f'https://www.amazon.es/deals?ref_=nav_cs_gb&deals-widget=%257B%2522version%2522%253A1%252C%2522viewIndex%2522%253A0%252C%2522presetId%2522%253A%2522deals-collection-all-deals%2522%252C%2522departments%2522%253A%255B%2522{cat_id}%2522%255D%252C%2522sorting%2522%253A%2522BY_DISCOUNT_DESCENDING%2522%257D'
        web_content = requests.get(url, headers=header)

        if web_content.status_code == 200:
            # identy start of json with the content
            i = web_content.text.find("{\"widgetId\"")
            partial_res = web_content.text[i:]
            f = partial_res.find('</script>') - 36
            parsed = json.loads(partial_res[:f])
            if (len(parsed['prefetchedData']['aapiGetDealsList'])) > 0:
                starting = parsed['prefetchedData']['aapiGetDealsList'][0]

            for product in starting['entities']:
                try:
                    if product['entity']['badge']['entity']['label']['content']['fragments'][0].get(
                            'text') != 'Hasta un -':
                        if cnt_products_per_cat < 3:
                            url_product = 'https://www.amazon.es' + product['entity']['details']['entity']['landingPage']['url']
                            deal_price = product['entity']['details']['entity']['price']['details']['dealPrice']['moneyValueOrRange']['value']['amount']
                            old_price = product['entity']['details']['entity']['price']['details']['basisPrice']['moneyValueOrRange'][ 'value']['amount']
                            discount = product['entity']['details']['entity']['price']['details']['savings']['percentage']['value']

                            if utils_botize.is_valid(url_product, deal_price, old_price, discount) \
                                    and url_product not in anteriores_url_anadidas:

                                query = f"INSERT INTO productos VALUES ('','{url_product}','{deal_price}','{old_price}','{discount}','{date.today()}','{cat_name}',0)"
                                # print(query)
                                print(url_product, deal_price, old_price, discount)
                                anteriores_url_anadidas.append(url_product)
                                utils_botize.connectDB(query, 'w')
                                cnt_products_per_cat = cnt_products_per_cat + 1
                        else:
                            break
                except Exception as e:
                    continue


get_content(header)
