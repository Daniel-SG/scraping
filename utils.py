import csv
import random
from datetime import date


    # 'Alimentacion_bebidas' 6198072031
    # Limpieza 2165679031
    # Audio y video portatil
    # Auriculares equipo de audio
    # Bebe 1703495031
    # Belleza 6198055031
    # Bricolaje 2454133031
    # CD y vinilos 599373031
    # Cerveza 6347711031
    # Climatizacion 3605952031
    # Coche y moto 1951051031
    # Comunicacion 6348071031
    # Limpieza 665492031
    # Deportes 2454136031
    # Dispositivos amazon 599370031
    # Electronica 827230031
    # Equipaje 599391031
    # Fotografia 4772050031
    # Grandes electrodomesticos 664660031
    # Hogar y cocina 12710835031

categories = {1:6198072031,2:2165679031,3:665477031,4:934056031,5:1703495031,6:6198055031,7:2454133031,8:599373031,
                  9:6347711031,10:3605952031,11:1951051031,12:6348071031,13:665492031,14:2454136031,15:599370031,
                  16:827230031,17:599391031,18:4772050031,19:664660031,20:12710835031}

def write_log(entry):
    if entry:
        f = open("log.csv", "a")
        f.write(entry + ',' + str(date.today()) + "\n")
        f.close()

def read_log():
    used = []
    with open('log.csv', newline='') as csvfile:
        log_list = csv.reader(csvfile, delimiter=',')
        for row in log_list:
            if row:
                used.append(row[0])
    return used

def get_amazon_categories():
    num = random.randrange(1, len(categories))
    return categories[num]
