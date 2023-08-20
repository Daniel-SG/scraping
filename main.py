import requests
from lxml import html

header = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36",
}

url = "https://www.blogdechollos.com/"

web_content = requests.get(url, headers=header)

parser = html.fromstring(web_content.text)

i = 1

while i < 20:
    pattern_product = f"//*[@id='main']/div/div/div[{i}]/div[3]/a/@href"
    url_product = str(parser.xpath(pattern_product))
    pattern_price = f'//*[@id="main"]/div/div/div[{i}]/div[3]/div[2]/div[1]/text()'
    pattern_old_price = f'//*[@id="main"]/div/div/div[{i}]/div[3]/div[2]/div[2]/div[1]/text()'

    if url_product.__contains__('https://www.amazon.es'):
        amazon_url = url_product[2:url_product.find('?')]
        response = requests.get(amazon_url,headers=header)
        if response.status_code == 200:
            price = str(parser.xpath(pattern_price)[0])
            old_price = str(parser.xpath(pattern_old_price)[0])
            print(amazon_url)
            print('current_price ' + price)
            print('old_price ' + old_price)
    i = i + 1

