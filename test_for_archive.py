import csv
import zipfile
from zipfile import ZipFile, ZIP_DEFLATED
import os

import pytest


@pytest.fixture()
def create_zip():
    #Путь к файлу zip
    zip_path = 'resources/file_zip'

    #Удаляем файл, если он существует
    if os.path.exists(zip_path):
        os.remove(zip_path)

    with ZipFile(zip_path, 'w', compression=ZIP_DEFLATED, compresslevel=5) as myzip:
        for folder, subfolders, files in os.walk('resources'):
            for file in files:
                if file.endswith(('.csv', '.xlsx', '.pdf')):
                    myzip.write(os.path.join(folder, file),
                                os.path.relpath(os.path.join(folder, file), 'resources'),
                                compress_type=zipfile.ZIP_DEFLATED)


def test_check_count_row_csv(create_zip):
    row_count_arc = 0
    with open('resources/example_one.csv', 'r') as f:
        file = csv.reader(f, delimiter=";")
        row_count = sum(1 for row in file)
    with ZipFile('resources/file_zip') as myzip:
        with myzip.open('example_one.csv', 'r') as myfile:
            for line in myfile:
                row_count_arc += 1
    assert row_count == row_count_arc, "Количество строк не совпадает"





