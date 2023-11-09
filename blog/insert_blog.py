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


def buildHtml(title, precio_actual, precio_anterior, descuento, foto_url,descripcion, url):
    descripcion = str(descripcion).replace('\n', '<br>')
    html = f"""
    
     
<body>
    <div class="product" style="background-color: #fff; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); border-radius: 10px; margin: 20px auto; padding: 20px; max-width: 400px;">
        <img src="{foto_url}" alt="Product Image" style="max-width: 100%; border-radius: 5px;">
        <h2 class="product-title" style="font-size: 24px; color: #333; margin: 10px 0;">{title}</h2>
        <p class="product-price" style="font-size: 20px; color: #d10000;">Current Price: {precio_actual}</p>
        <p class="product-old-price" style="font-size: 16px; color: #777; text-decoration: line-through;">Old Price: {precio_anterior}</p>
        <p class="product-discount" style="font-size: 18px; color: #009900; font-weight: bold;">Descuento: {descuento}</p>
        <p class="product-description" style="font-size: 16px; color: #444; margin-top: 20px;"><b>Descripción:</b><br> {descripcion}</p>
        <a class="buy-button" href="{url}" target="_blank" style="display: inline-block; background-color: #ff9900; color: #fff; padding: 10px 20px; font-size: 18px; text-decoration: none; border-radius: 5px; margin-top: 20px; transition: background-color 0.3s;">Buy on Amazon</a>
    </div>
</body>
</html>

             
    """

    return html


def format_post(title, precio_actual, precio_anterior, descuento, foto_url, descripcion, url):
    title_post = title

    customMetaData = "This is meta data"
    payload = {
        "content": buildHtml(title, precio_actual, precio_anterior, descuento, foto_url,descripcion, url),
        "title": title_post,
        'labels': ['label1', 'label2'],
        'customMetaData': customMetaData
    }
    postToBlogger(payload)
    sleep(10)

