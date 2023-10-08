from selenium import webdriver
from selenium.webdriver.common.by import By

from utils_amzn_selenium import get_title, get_currentPrice, get_descuento, get_precio_anterior, get_descripcion, \
    get_foto_url


def product_set(driver):
    products = []
    products_list = driver.find_elements(By.CLASS_NAME, "a-list-item")

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

    driver.quit()
    sorted_products = sorted(products, key=lambda discount: discount[0], reverse=True)
    if sorted_products[0][2]:
        specific_product(driver, sorted_products[0])


def specific_product(driver, product):
    if product:
        driver = webdriver.Firefox()
        driver.get(product[2])
        cookies = driver.find_element(By.CSS_SELECTOR, '#sp-cc-accept')
        cookies.click()
    title = get_title(driver)
    print(title)

    precio_actual = get_currentPrice(driver)
    print(precio_actual)
    descuento = get_descuento(driver)
    print(descuento)
    precio_anterior = get_precio_anterior(driver)
    print(precio_anterior)
    descripcion = get_descripcion(driver)
    print(descripcion)
    foto_url = get_foto_url(driver)
    print(foto_url)

    driver.quit()


def amazn_scrap_selenium(url):
    url = 'https://www.amazon.es/deal/dd20fde3?'
    url = 'https://www.amazon.es/Oral-B-Cepillos-El%C3%A9ctricos-Recargables-Recambio/dp/B0B4WSC72G'

    driver = webdriver.Firefox()
    driver.get(url)
    cookies = driver.find_element(By.CSS_SELECTOR, '#sp-cc-accept')
    cookies.click()

    try:
        # Si es la pagina de un producto concreto, la llamada no fallara
        driver.find_element(By.CLASS_NAME, 'a-section.a-spacing-none.aok-align-center')
        specific_product(driver, '')


    except Exception as e:
        # Si salta la excepcion es porque es una pagina que contiene varios productos
        product_set(driver)
