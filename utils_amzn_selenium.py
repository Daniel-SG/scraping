from selenium.webdriver.common.by import By


def get_title(driver):
    try:
        title = driver.find_element(By.ID, "title")
    except Exception as e:
        print(e)

    return title.text


def get_currentPrice(driver):
    try:
        current_price = driver.find_element(By.CLASS_NAME, "a-offscreen").text

        if not current_price:
            current_price = driver.find_element(By.CLASS_NAME,
                                                "a-price.aok-align-center.reinventPricePriceToPayMargin.priceToPay")
            precio_entero = str(current_price.text).split('\n')[0]
            precio_decimal = str(current_price.text).split('\n')[1]
            current_price = precio_entero + ',' + precio_decimal

    except Exception as e:
        print(e)

    return current_price


def get_precio_anterior(driver):
    try:
        #precio_anterior_arr = driver.find_elements(By.CLASS_NAME, "a-price.a-text-price")
        #if len(precio_anterior_arr)>2:
        #    precio_anterior = precio_anterior_arr[3]
        #else:
        #    precio_anterior = precio_anterior_arr[0]
        precio_anterior = driver.find_elements(By.CLASS_NAME, "a-size-small.a-color-secondary.aok-align-center.basisPrice")[0]
    except Exception as e:
        print(e)

    return precio_anterior.text.replace('Precio anterior: ','')


def get_descuento(driver):
    try:
        descuento = driver.find_element(By.CLASS_NAME,
                                        "a-size-large.a-color-price.savingPriceOverride.aok-align-center.reinventPriceSavingsPercentageMargin.savingsPercentage")
    except Exception as e:
        print(e)

    return descuento.text


def get_descripcion(driver):
    try:
        descripcion = driver.find_element(By.CLASS_NAME, "a-unordered-list.a-vertical.a-spacing-mini")
    except Exception as e:
        print(e)

    return descripcion.text


def get_foto_url(driver):
    try:
        url = driver.find_element(By.ID, "landingImage").get_attribute('src')
    except Exception as e:
        print(e)

    return url
