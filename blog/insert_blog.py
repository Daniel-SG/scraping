from time import sleep

import httplib2
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run_flow
from googleapiclient import discovery


# https://www.youtube.com/watch?v=to461lvKMqY
# Start the OAuth flow to retrieve credentials
def authorize_credentials():
    CLIENT_SECRET = 'blog/client_secrets.json'
    SCOPE = 'https://www.googleapis.com/auth/blogger'
    STORAGE = Storage('credentials.storage')
    # Fetch credentials from storage
    credentials = STORAGE.get()

    # If the credentials doesn't exist in the storage location then run the flow
    if credentials is None or credentials.invalid:
        flow = flow_from_clientsecrets(CLIENT_SECRET, scope=SCOPE)
        http = httplib2.Http()
        credentials = run_flow(flow, STORAGE, http=http)
    return credentials


# print(credentials)
def getBloggerService():
    credentials = authorize_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://blogger.googleapis.com/$discovery/rest?version=v3')
    service = discovery.build('blogger', 'v3', http=http, discoveryServiceUrl=discoveryUrl)
    return service


def postToBlogger(payload):
    service = getBloggerService()
    post = service.posts()
    insert = post.insert(blogId='1828568334147672773', body=payload).execute()
    print("Done post!")

    return insert


def buildHtml(currentPrice, oldPrice, descuento, descripcion, url):
    html = f'Antes: <h1>{oldPrice}</h1>' \
           f' \n Ahora: <h1>{currentPrice}</h1> ' \
           f' \n Descuento:  <h2> {descuento}</h2> ' \
           f' \n Descripcion: <h2> {descripcion}</h2>' \
           f' \n url: <h2>{url} </h2>'
    return html


def format_post(title, precio_actual, precio_anterior, descuento, foto_url, descripcion, url):
    title_post = title

    customMetaData = "This is meta data"
    payload = {
        "content": buildHtml(precio_actual, precio_anterior, descuento, descripcion, url),
        "title": title_post,
        'labels': ['label1', 'label2'],
        'customMetaData': customMetaData
    }
    postToBlogger(payload)
    sleep(10)

