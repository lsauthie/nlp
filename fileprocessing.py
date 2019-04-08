# This module is in charge of managing files
import csv
import json
from pathlib import Path
import os

home = Path(__file__).parents[0]

def read_csv(filename):
    list_file = []
    
    with open(home / filename, 'r', encoding="utf-8-sig") as f:
        reader = csv.reader(f, delimiter=';')
        list_file = list(reader)
    
    return list_file


def write_csv(filename, list_file):
    
    while True:
        try:
            output = open(home / filename, 'w', newline='', encoding='utf-8-sig')
            break
        except PermissionError:
            input("Please close the file: " + filename + " and click enter!")
        
    
    output_writer = csv.writer(output, delimiter=';')
    
    for i in list_file:
        output_writer.writerow(i)

    output.close()

#write configuration information
def read_json():
    
    with open(home / 'config.json') as json_data_file:
        data = json.load(json_data_file)
    
    return data

def write_json(data):
    
    with open(home / 'config.json', 'w') as outfile:
        json.dump(data, outfile)
