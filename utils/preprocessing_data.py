import os
import re
import csv
import pandas as pd


def replace_symbol(string):
    TOKEN_SYMBOLS = ["\n", "\xa0"]
    for symbol in TOKEN_SYMBOLS:
        string = string.replace(symbol, "")

    return string


def drop_none(data):
    print(len(data))
    dataframe = pd.DataFrame(data)
    dataframe = dataframe.dropna()
    return dataframe.values.tolist()


def save_to_csv(data, file_path):
    with open(file_path, "w", encoding="windows-1251") as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=",")
        for i in data:
            csv_writer.writerow(i)


def csv_to_array(file_path):
    array = []
    with open(file_path, 'r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            array.append(row)
    return array


def remove_duplicates_from_column(data, index):
    column = [row[index] for row in data]
    unique_column = list(set(column))
    unique_data = []

    for row in data:
        if row[index] in unique_column:
            unique_data.append(row)
            unique_column.remove(row[index])

    return unique_data


def find_numbers(text):
    numbers = re.findall(r"[-+]?\d+\.\d+|\d+", text)
    return numbers


def data_to_csv(data, current_dir, name_of_csv_file, url):
    with open(fr"{current_dir}\{name_of_csv_file}_{url[-1]}.csv",
              mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        for row in data:
            writer.writerow(row)


def check_empty_files(directory):
    empty_files = []
    files = os.listdir(directory)
    for file in files:
        with open(os.path.join(directory, file),
                  mode="r", encoding="utf-8") as csv_file:
            csv_reader = csv.reader(csv_file)
            rows = list(csv_reader)
            if len(rows) == 0:
                empty_files.append(file.split(".")[0][-1])
            else:
                print("[+] file not empty")

    return empty_files

