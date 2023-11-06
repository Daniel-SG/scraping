
# Amazon Scraper

## Description
Given a deal **url** from amazon.es it will return the highest discounted product from the page.
* It will return the product with this data as python dict:
* ```Python Data Dict
  {
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
  ```

## Installation
1. download and intall chrome or edge browser
2. download and install the corresponding webdriver
    * [chromedriver](https://chromedriver.chromium.org/downloads) or [googlechromelabs](https://googlechromelabs.github.io/chrome-for-testing/)
    * [edge](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/)
3. Clone or download the Project
4. install the requirements
    * Must have python 3.9 or higher [python](https://www.python.org/downloads/)
    * run this command in the terminal
    ```bash
      pip install -r requirements.txt
    ```

## Usage
* if you pass url in the constructor then you can run the scraper with the run method
* default browser is edge
* default executable_path is set to drivers/edge/msedgedriver.exe
* if output_file set to None then it will not save the data in json file

```Python
from amazon_scraper import AmazonScraper


amazon_scraper = AmazonScraper(url=None, 
                               postal_code=28013, 
                               implisit_wait_time=0.1, 
                               output_file='product_data.json', 
                               is_headless=False,
                               browser=None, 
                               executable_path=None)

url = 'https://www.amazon.es/deals?deals-widget=%257B%2522version%2522%253A1%252C%2522viewIndex%2522%253A0%252C%2522presetId%2522%253A%2522deals-collection-all-deals%2522%252C%2522departments%2522%253A%255B%2522599370031%2522%255D%252C%2522sorting%2522%253A%2522FEATURED%2522%257D'

data = amazon_scraper.run(url)