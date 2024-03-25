import json
import os
import mysql.connector
import requests

categories = {6198073031: 'Alimentación y bebidas',
              2165679031: 'Aspiración, limpieza y cuidado de suelo y ventanas',
              665477031: 'Audio y vídeo portátil',
                1703495031: 'Bebé',
              6198055031: 'Belleza',
2454133031: 'Bricolaje y herramientas',
6347711031: 'Cervezas, vinos y licores',3605952031: 'Climatización y calefacción',

6348071031: 'Cuidado y limpieza del hogar',2454136031: 'Deportes y aire libre',
599370031: 'Electrónica',
12710835031: 'Equipaje y accessorios de viaje',664660031: 'Fotografía y videocámaras',
4772050031: 'Grandes electrodomésticos',
599391031: 'Hogar y cocina',
3564289031: 'Iluminación',

667049031: 'Informática',
3628866031: 'Instrumentos musicales',1571260031: 'Jardín',
10440402031: 'Joyería para hombre',10440373031: 'Joyería para mujer',
599385031: 'Juguetes y juegos',
5512276031: 'Moda',
5518994031: 'Moda Bebé',
5518992031: 'Moda Niña',
5518993031: 'Moda Niño',
2822691031: 'Muebles de hogar',
3628728031: 'Oficina y papelería',
599379031: 'Películas y TV',
12472654031: 'Productos para mascotas',
10117368031: 'Relojes para hombre',
10117375031: 'Relojes para mujer',
3677430031: 'Salud y cuidado personal',
664659031: 'TV, vídeo y home cinema',
4347039031: 'Vitaminas, minerales y suplementos en medicamentos, remedios y suplementos dietéticos'}


categories_bck = {6198073031: 'Alimentación y bebidas',2165679031: 'Aspiración, limpieza y cuidado de suelo y ventanas',
665477031: 'Audio y vídeo portátil',934056031: 'Auriculares para equipo de audio',
1703495031: 'Bebé',6198055031: 'Belleza',
2454133031: 'Bricolaje y herramientas',599373031: 'CDs y vinilos',
6347711031: 'Cervezas, vinos y licores',3605952031: 'Climatización y calefacción',
1951051031: 'Coche y moto',665492031: 'Comunicación móvil y accesorios',
6348071031: 'Cuidado y limpieza del hogar',2454136031: 'Deportes y aire libre',
827230031: 'Dispositivos Amazon',599370031: 'Electrónica',
12710835031: 'Equipaje y accessorios de viaje',664660031: 'Fotografía y videocámaras',
4772050031: 'Grandes electrodomésticos',
599391031: 'Hogar y cocina',
3564289031: 'Iluminación',
5866088031: 'Industria, empresas y ciencia',
667049031: 'Informática',
3628866031: 'Instrumentos musicales',1571260031: 'Jardín',
10440402031: 'Joyería para hombre',10440373031: 'Joyería para mujer',
599385031: 'Juguetes y juegos',
599364031: 'Libros',
5512276031: 'Moda',
5518994031: 'Moda Bebé',
5518992031: 'Moda Niña',
5518993031: 'Moda Niño',
2822691031: 'Muebles de hogar',
3628728031: 'Oficina y papelería',
599379031: 'Películas y TV',
2165660031: 'Planchas, centros de planchado y accesorios',
12472654031: 'Productos para mascotas',
10117368031: 'Relojes para hombre',
10117375031: 'Relojes para mujer',
3677430031: 'Salud y cuidado personal',
599376031: 'Software',
664659031: 'TV, vídeo y home cinema',
818936031: 'Tienda Kindle',
599382031: 'Videojuegos',
4347039031: 'Vitaminas, minerales y suplementos en medicamentos, remedios y suplementos dietéticos'}


def is_valid(url, deal, old_price, discount):
    return url != '' and deal != '' and old_price != '' and discount != '' and discount > 29


def connectDB(query, operation='r'):
    mydb = mysql.connector.connect(
        host='193.203.168.5',
        user='u559223161_descuentino',
        password='MuadcorL1!QC',
        database='u559223161_botize'
    )

    mycursor = mydb.cursor()

    if operation == 'r':
        mycursor.execute(query)
        myresult = mycursor.fetchall()

        return myresult

    else:
        mycursor.execute(query)
        mydb.commit()
        print(mycursor.rowcount, "record inserted.")


def update_categories():
    header = ({'User-Agent':
                   'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 '
                   'Safari/537.36',
               'Accept-Language': 'en-US, en;q=0.5'})
    url = f'https://www.amazon.es/events/springdealdays?ref_=nav_cs_gb_td_ss_dt_cr&deals-widget=%257B%2522version%2522%253A1%252C%2522viewIndex%2522%253A0%252C%2522presetId%2522%253A%2522deals-collection-all-deals%2522%252C%2522departments%2522%253A%255B%25226198073031%2522%255D%252C%2522sorting%2522%253A%2522FEATURED%2522%257D'

    web_content = requests.get(url, headers=header)
    # identy start of json with the content
    i = web_content.text.find("{\"widgetId\"") + 3
    partial_res = web_content.text[i:]

    # second widgetid
    i = partial_res.find("{\"widgetId\"")
    partial_res = partial_res[i:]

    f = partial_res.find('</script>') - 36
    parsed = json.loads(partial_res[:f])
    if (len(parsed['prefetchedData']['aapiGetDealsList'])) > 0:
        starting = parsed['prefetchedData']['aapiSearchDeals']['entity']['refinements'][0]['departments']['options']
        for s in starting:
            print(s['filter']['department'] + ': \'' + s['name']['fragments'][0]['text'] + '\',')

