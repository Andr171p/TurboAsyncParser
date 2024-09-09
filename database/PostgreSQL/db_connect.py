import os
import csv
import time
import psycopg2
from datetime import datetime
from utils.preprocessing_data import remove_duplicates_from_column, drop_none
from database.PostgreSQL.db_auth_data import host, user, password, db_name, port


def csv_to_array(directory):
    files = []
    data = []
    # directory = r"C:\Users\andre\TyuiuProjectParser\TurboAsyncParser\data\avito\pages\selhoznaznacheniya"
    for filename in os.listdir(directory):
        files.append(filename)
    for i in range(len(files)):
        with open(os.path.join(directory, files[i]),
                  "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            for row in reader:
                data.append(row)

    return data


def convert_data(data):
    for row in data:
        row[1] = int(row[1])
        try:
            row[2] = float(row[2])
        except Exception as _ex:
            print(_ex)
            row[2] = None
        try:
            row[4] = datetime.strptime(row[4], '%Y-%m-%d').date()
        except Exception as _ex:
            print(_ex)
            row[4] = datetime.strptime(row[4], '%Y-%m-%d %H:%M:%S').date()
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


def data_upload(timeout=15):
    dir_list = [
        r"C:\Users\andre\TyuiuProjectParser\TurboAsyncParser\data\sova\pages\kommercheskaya",
        r"C:\Users\andre\TyuiuProjectParser\TurboAsyncParser\data\sova\pages\uchastok"
    ]
    for directory in dir_list:
        data = csv_to_array(directory=directory)
        data = convert_data(data=data)
        data = drop_none(data=data)
        data = remove_duplicates_from_column(
            data=data,
            index=5
        )
        print(len(data))
        db_connect(data_parser=data)
        time.sleep(timeout)


def main():
    data_upload()


if __name__ == "__main__":
    main()

