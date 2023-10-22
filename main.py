from operator import itemgetter

import amzn_partes
import amzn_selenium
from utils import read_log

header = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36",
}

used_links = read_log()
# blogdechollos_handler.scraping(header, used_links)
# ofertitas_handler.scraping(header,used_links)
# amz_v1.scraping(header, used_links)
amzn_partes.scraping(used_links)


