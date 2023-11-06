import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from msedge.selenium_tools import Edge, EdgeOptions
from bs4 import BeautifulSoup


class AmazonScraper:
    def __init__(self, url=None, postal_code=28013, implisit_wait_time=0.1, output_file='product_data.json', is_headless=False,
                 browser=None, executable_path=None):
        self.url = url
        self.postal_code = postal_code
        self.is_postal_code_changed = False
        self.driver = None
        self.implisit_wait_time = implisit_wait_time
        self.soup = None
        self.output_file = output_file
        self.executable_path = executable_path
        self.browser = browser if browser is not None else 'edge'
        self.options = None
        self.is_headless = is_headless
        self.product_data = {
            'asin': '',
            'url': '',
            'detail_url': '',
            'image_url': '',
            'name': '',
            'title': '',
            'original_price': '',
            'discount': '',
            'discouted_price_whole': '',
            'discouted_price_fraction': '',
            'discouted_price_symbol': '',
            'discouted_price': '',
            'heading': '',
            'description': '',
        }

    def __driver_init__(self):
        print('Initializing driver...')
        if self.executable_path is None:
            self.executable_path = 'drivers/chromedriver.exe' if self.browser == 'chrome' else 'drivers/msedgedriver.exe'

        self.options = Options() if self.browser == 'chrome' else EdgeOptions()
        self.options.add_argument("--disable-notifications")
        self.options.add_argument("--disable-infobars")
        self.options.add_argument("--mute-audio")
        self.options.add_argument("--disable-popup-blocking")
        if self.is_headless:
            self.options.use_chromium = True
            self.options.add_argument("--headless")
            self.options.add_argument("--disable-gpu")
            self.options.add_argument("--no-sandbox")
            self.options.add_argument("--window-size=1920,1080")
        try:
            if self.browser == 'chrome':
                self.driver = webdriver.Chrome(executable_path=self.executable_path, options=self.options)
            elif self.browser == 'edge':
                self.driver = Edge(executable_path=self.executable_path, options=self.options)
            else:
                raise Exception('Browser not supported')
        except Exception as e:
            print(e)
            raise Exception(f'Driver not initialized: {e}')

    def wait_for_page_load(self):
        print("Waiting For page to load...")
        page_state = self.driver.execute_script('return document.readyState;')
        count = 0
        while page_state != 'complete' and count < 10:
            self.implicitly_wait()
            page_state = self.driver.execute_script('return document.readyState;')
            count += 1

    def get(self, url, params=None, headers=None, ):
        print('Getting URL and initializing soup...')
        self.driver.get(url)
        self.implicitly_wait()
        # self.wait_for_page_load()
        self.cc_accept()
        # if not self.is_postal_code_changed:
        self.change_postal_code()
        self.toggle_scroll()
        self.soup = BeautifulSoup(self.driver.page_source, 'html.parser')

    def implicitly_wait(self):
        self.driver.implicitly_wait(self.implisit_wait_time)

    def scroll_down(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        self.implicitly_wait()

    def scroll_up(self):
        self.driver.execute_script("window.scrollTo(0, 0);")
        self.implicitly_wait()

    def toggle_scroll(self):
        self.scroll_down()
        self.scroll_up()

    def cc_accept(self, ):
        ret, cc_accept = self.wait_for_element("sp-cc-accept", by=By.ID)
        if ret:
            cc_accept.click()
            self.implicitly_wait()

    def is_postal_code_same(self):
        ret, ele = self.wait_for_element('glow-ingress-line2', by=By.ID)
        if not ret:
            return False

        return str(self.postal_code) in ele.text


    def change_postal_code(self):
        if not self.is_postal_code_same():
            ret, ele = self.wait_for_element("nav-global-location-popover-link", by=By.ID)
            if ret:
                ele.click()
                self.implicitly_wait()
                ret, ele = self.wait_for_element("GLUXZipUpdateInput", by=By.ID)
                if ret:
                    ele.send_keys(self.postal_code)
                    ele.send_keys(Keys.ENTER)
                    self.implicitly_wait()
                    self.is_postal_code_changed = True
                    return True
                else:
                    return False
            else:
                return False

    def wait_for_element(self, xpath, by=By.TAG_NAME):
        try:
            ele = self.driver.find_elements(by, xpath)
            count = 0
            while len(ele) == 0 and count < 10:
                self.implicitly_wait()
                ele = self.driver.find_elements(by, xpath)
                count += 1

            return True, ele[0]
        except:
            return False, None

    def image_to_text(self, img_url):
        pass

    def find_solve_capcha(self):
        ret, ele = self.wait_for_element("recaptcha-anchor", by=By.ID)
        if ret:
            img_url = ele.get_attribute('src')
            text = self.image_to_text(img_url)

            ret, ele = self.wait_for_element("recaptcha-input", by=By.ID)
            if ret:
                ele.send_keys(text)
                ele.send_keys(Keys.ENTER)
                return True
            else:
                return False
        else:
            return True

    def get_product_list(self):
        product_div = self.soup.find('div', attrs={'data-testid': 'grid-deals-container'})
        product_list = product_div.find_all('div', attrs={'data-testid': 'deal-card'})
        return product_list

    def find_product_details(self):
        print('Getting product details...')
        title_list = self.soup.find_all('span', attrs={'id': 'productTitle'})
        if len(title_list) > 0:
            title = title_list[0].text
        else:
            return 'find_next'
        price_div = self.soup.find('div', attrs={'id': 'corePriceDisplay_desktop_feature_div'})
        if price_div is not None:
            discounted_price_whole = self.soup.find('span', attrs={'class': 'a-price-whole'}).text
            discounted_price_whole = discounted_price_whole.replace(',', '')
            discounted_price_fraction = self.soup.find('span', attrs={'class': 'a-price-fraction'}).text
            discounted_price_symbol = self.soup.find('span', attrs={'class': 'a-price-symbol'}).text
            discounted_price = f'{discounted_price_whole},{discounted_price_fraction} {discounted_price_symbol}'
            original_price = price_div.find('span',
                                            attrs={'class': 'a-price a-text-price',
                                                   'data-a-strike': "true"
                                                   }).find('span').text
        else:
            core_price_desktop = self.soup.find('div', attrs={'id': 'corePrice_desktop'})
            if core_price_desktop is not None:
                price_table = core_price_desktop.find('table')
                if price_table is not None:
                    price_td = price_table.find_all('td')
                    if len(price_td) > 0:
                        original_price = price_td[1].find('span',attrs={'aria-hidden':"true"}).text
                        discounted_price_text = price_td[3].find('span',attrs={'aria-hidden':"true"}).text
                        discounted_price_text = discounted_price_text.replace('€', '')
                        discounted_price_whole = discounted_price_text.split(',')[0]
                        discounted_price_fraction = discounted_price_text.split(',')[1].split(' ')[0]
                        discounted_price_symbol = '€'
                        discounted_price = f'{discounted_price_whole},{discounted_price_fraction} {discounted_price_symbol}'
                    else:
                        return 'find_next'
                else:
                    return 'find_next'
            else:
                return 'find_next'

        heading = ''
        description = ''
        description_bullets = self.soup.find_all('div', attrs={'id': 'feature-bullets'})
        product_facts = self.soup.find_all('div', attrs={'id': 'productFactsDesktopExpander'})
        if len(description_bullets) > 0:
            heading_list = description_bullets[0].find_all('h1')
            if len(heading_list) > 0:
                heading = description_bullets[0].find('h1').text
            description_list = description_bullets[0].find_all('li')
            description = ''
            for desc in description_list:
                description += desc.text + '\n'
        elif len(product_facts) > 0:
            heading_list = product_facts[0].find_all('h3')
            if len(heading_list) > 0:
                heading = heading_list[-1].text

            description_list = product_facts[0].find_all('li')
            description = ''
            for desc in description_list:
                description += desc.text + '\n'

        print('Product details found: Almost There...')
        self.product_data['title'] = title.strip()
        self.product_data['discouted_price_whole'] = discounted_price_whole.strip()
        self.product_data['discouted_price_fraction'] = discounted_price_fraction.strip()
        self.product_data['discouted_price_symbol'] = discounted_price_symbol.strip()
        self.product_data['discouted_price'] = discounted_price.strip()
        self.product_data['original_price'] = original_price.strip()
        self.product_data['heading'] = heading.strip()
        self.product_data['description'] = description.strip()

        return 'details_found'

    def find_high_discount_product(self, product_list):
        highest_discount_product = None
        highest_discount = 0
        print('Total Products in Page 1: ', len(product_list), 'Finding highest discount product...')
        for product in product_list:
            discount_span = product.find('span', attrs={'aria-live': 'off'})
            discount_div = discount_span.find('div')
            discount_text = discount_div.text
            if 'Hasta un' in discount_text or 'Upp till' in discount_text or '%' not in discount_text:
                continue
            discount = discount_text.split('%')[0]
            discount = discount.replace('Upp till', '')
            discount = abs(int(discount))
            if discount > highest_discount:
                highest_discount = discount
                highest_discount_product = product

        if highest_discount_product is not None:
            print('Highest Discount Found: ', highest_discount)
            a_tags = highest_discount_product.find_all('a')
            detail_url = a_tags[-1].get('href')
            asin = detail_url.split('?')[0].split('/')[-1]
            name = a_tags[-1].text
            self.get(detail_url)
            product_details = self.find_product_details()
            if product_details == 'find_next':
                print('Product Detail Does not had discount: Finding next highest discount product...\n')
                product_list.remove(highest_discount_product)
                self.find_high_discount_product(product_list)
            else:
                self.product_data['detail_url'] = detail_url
                self.product_data['asin'] = asin
                self.product_data['name'] = name
                self.product_data['discount'] = highest_discount
                self.product_data['image_url'] = highest_discount_product.find('img').get('src')

    def run(self, url=None):
        # try:

        if self.url is None and url is None :
            raise Exception('URL is required')


        if url is not None:
            self.url = url

        main_url = self.url
        self.__driver_init__()
        self.get(self.url)


        product_list = self.get_product_list()
        self.find_high_discount_product(product_list)

        self.product_data['url'] = main_url

        if self.output_file is not None:
            self.output_file = f'{self.output_file}.json' if not self.output_file.endswith('.json') else self.output_file
            print(f'Product details found: Saving to file in {self.output_file}')
            with open(self.output_file, 'w') as f:
                json.dump(self.product_data, f, indent=4)

        self.driver.close()
        return self.product_data
        # except Exception as e:
        #     logging.error(e)
        #     print(e)
        #     self.driver.close()
        #     return f'error {e}'

