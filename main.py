from operator import itemgetter

import amzn_partes
import amzn_selenium
from blog.insert_blog import format_post
from utils import read_log

used_links = read_log()

amzn_partes.scraping(used_links)

title='esto es un titulo'
precio_actual = 10
precio_anterior = 20
descuento = '50%'
foto_url = 'https://phantom-marca.unidadeditorial.es/0dc642a404bc4b913a8108ba62041e33/resize/660/f/webp/assets/multimedia/imagenes/2023/11/09/16995642859044.jpg'
descripcion='esto es una descripcion'
url='www.google.es'
#format_post(title, precio_actual, precio_anterior, descuento, foto_url, descripcion, url)


