import os
import mysql.connector


categories = {6198073031: 'Alimentacion_bebidas', 665477031: 'Audio y video portatil',
                  1703495031: 'Bebe', 1703495031: 'Belleza',
                  665492031: 'comunicacion', 5518994031: 'Limpieza', 2454136031: 'Deportes',
                  599391031: 'Equipaje', 4772050031: 'Fotografia', 664660031: 'Grandes electrodomesticos',
                  12710835031: 'Hogar y cocina', 3564289031: 'iluminacion', 667049031: 'Informática',
                  1571259031: 'Jardín', 10440402031: 'Joyería para hombre', 599385031: 'Joyería para mujer',
                  5518992031: 'Moda', 5518994031: 'Moda Bebé', 827230031: 'Electronica', 3605952031: 'Climatizacion',
                  3628866031: 'Intrumentos musicales', 1571260031: 'Jardin', 599364031: 'Juguetes y juegos',
                  10440373031: 'Moda Niña'}

categories_bck = {6198073031: 'Alimentacion_bebidas', 665477031: 'Audio y video portatil',
                  1703495031: 'Bebe', 1703495031: 'Belleza', 2454133031: 'Bricolaje',
                  6347711031: 'Cerveza', 1951051031: 'Coche y moto',
                  665492031: 'comunicacion', 5518994031: 'Limpieza', 2454136031: 'Deportes',
                  599391031: 'Equipaje', 4772050031: 'Fotografia', 664660031: 'Grandes electrodomesticos',
                  12710835031: 'Hogar y cocina', 3564289031: 'iluminacion', 667049031: 'Informática',
                  1571259031: 'Jardín', 10440402031: 'Joyería para hombre', 599385031: 'Joyería para mujer',
                  5518992031: 'Moda', 5518994031: 'Moda Bebé', 827230031: 'Electronica', 3605952031: 'Climatizacion',
                  3628866031: 'Intrumentos musicales', 1571260031: 'Jardin', 599364031: 'Juguetes y juegos',
                  10440373031: 'Moda Niña'}


def is_valid(url, deal, old_price, discount):
    return url != '' and deal != '' and old_price != '' and discount != '' and discount > 29


def connectDB(query, operation='r'):
    mydb = mysql.connector.connect(
        host=os.environ['bd_host'],
        user=os.environ['bd_user'],
        password=os.environ['bd_pass'],
        database=os.environ['bd_name']
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


