from selenium import webdriver
from selenium.webdriver.common.by import By


def amazn_scrap_selenium(url):
    # url = 'https://www.amazon.es/deal/17ce50b2'
    products = []
    print(url)
    browser = webdriver.Firefox()
    browser.get(url)
    cookies = browser.find_element(By.CSS_SELECTOR, '#sp-cc-accept')
    cookies.click()

    # base = browser.find_element_by_class_name('a-section octopus-dlp-asin-section')
    products_list = browser.find_elements(By.CLASS_NAME, "a-list-item")

    for product in products_list:
        detalles = product.text.split('\n')
        titulo = detalles[0]
        descuento = detalles[3]
        precio_conjunto = detalles[5].split(' ')
        precio_actual = precio_conjunto[0]
        precio_anterior = precio_conjunto[3] + '€'
        url = product.find_element(By.CLASS_NAME, 'a-link-normal').get_attribute('href')
        l = (descuento, titulo, url)
        products.append(l)
        # print(descuento, precio_actual, precio_anterior)

    browser.quit()
    sorted_products = sorted(products, key=lambda discount: discount[0], reverse=True)
    print(sorted_products)


