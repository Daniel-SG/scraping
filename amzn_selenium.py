from selenium import webdriver
from selenium.webdriver.common.by import By


def amazn_scrap_selenium(url):
    url = 'https://www.amazon.es/deal/17ce50b2'
    browser = webdriver.Firefox()
    browser.get(url)
    cookies = browser.find_element(By.CSS_SELECTOR, '#sp-cc-accept')
    cookies.click()
    # base = browser.find_element_by_class_name('a-section octopus-dlp-asin-section')
    # base = browser.find_elements_by_css_selector('li.a-list-normal:nth-child(1) > span:nth-child(1) > div:nth-child(1)')
    # base = browser.find_element_by_class_name('a-list-item')
    base = browser.find_element(By.CLASS_NAME, "a-list-item")
    print(base.text)



    browser.quit()



amazn_scrap_selenium('')
