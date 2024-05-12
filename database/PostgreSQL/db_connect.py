import os
import csv
import psycopg2
from datetime import datetime
from database.PostgreSQL.db_auth_data import host, user, password, db_name, port


def csv_to_array():
    array = []
    directory = r"C:\Users\andre\TyuiuProjectParser\TurboAsyncParser\data\avito\pages\selhoznaznacheniya"
    for filename in os.listdir(directory):
        with open(os.path.join(directory, filename),
                  "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            for row in reader:
                array.append(row)
        return array


def convert_data(data):
    for row in data:
        row[1] = int(row[1])
        row[2] = float(row[2])
        row[4] = datetime.strptime(row[4], '%Y-%m-%d').date()
    return data


def db_connect(data_parser):

    connection = psycopg2.connect(
        dbname=db_name,
        user=user,
        password=password,
        host=host,
        port=port
    )
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO komerc (information, price, area, address, datas, url, category, cadastral_number, photo) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            for row in data_parser:
                cursor.execute(sql, row)
            connection.commit()
            print("[INFO] Data inserted successfully")
    except psycopg2.Error as _ex:
        print("[INFO] Error while working with PostgresSQL", _ex)
        connection.rollback()
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("[INFO] PostgresSQL connection closed")


d = csv_to_array()
d = convert_data(d)
print(d)
print(len(d))
db_connect(d)
