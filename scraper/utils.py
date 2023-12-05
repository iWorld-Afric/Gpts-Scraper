import csv
import os

def create_csv_file(path, headers):
    """ Create a CSV file with the given headers if it doesn't exist. """
    if not os.path.exists(path):
        with open(path, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(headers)
