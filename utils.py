import csv
from datetime import date


def write_log(entry):
    f = open("log.csv", "a")
    f.write("\n" + entry + ',' + str(date.today()))
    f.close()

def read_log():
    used = []
    with open('log.csv', newline='') as csvfile:
        log_list = csv.reader(csvfile, delimiter=',')
        for row in log_list:
            used.append(row[0])
    return used
