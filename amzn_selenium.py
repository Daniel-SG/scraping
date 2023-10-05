from selenium import webdriver
from selenium.webdriver.common.by import By


def product_set(browser):
    products = []
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


def specific_product(driver, base):
    title = driver.find_element(By.ID, "title")
    print(title)
    base = driver.find_element(By.CLASS_NAME, "a-offscreen")
    precio_entero = base.text.split('\n')
    descuento = precio_entero[0]
    descuento_sin_simbolo = descuento.replace('%', '')
    precio_actual = precio_entero[1] + ',' + precio_entero[2]
    print(descuento)
    print(precio_actual)

    driver.quit()

def amazn_scrap_selenium(url):
    url = 'https://www.amazon.es/AmazonBasics-S%C3%A1banas-Ajustables-190-Oscuro/dp/B00Q4TMEHS'

    browser = webdriver.Firefox()
    browser.get(url)
    cookies = browser.find_element(By.CSS_SELECTOR, '#sp-cc-accept')
    cookies.click()

    try:
        base = browser.find_element(By.CLASS_NAME, 'a-section.a-spacing-none.aok-align-center')


    except Exception as e:
        print(e)

    if base:
        print('see')
    else:
        print('noo')
    browser.quit()
