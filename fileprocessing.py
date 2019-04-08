# This module is in charge of managing files
import csv
import json
from pathlib import Path

home = 'C:/Users/tk4az/OneDrive/qna/program/'

def read_csv(filename):
    list_file = []
    
    with open(Path(home+filename), 'r', encoding="utf-8-sig") as f:
        reader = csv.reader(f, delimiter=';')
        list_file = list(reader)
    
    return list_file


def write_csv(filename, list_file):
    
    while True:
        try:
            output = open(Path(home+filename), 'w', newline='', encoding='utf-8-sig')
            break
        except PermissionError:
            input("Please close the file: " + filename + " and click enter!")
        
    
    output_writer = csv.writer(output, delimiter=';')
    
    for i in list_file:
        output_writer.writerow(i)

    output.close()

#write configuration information
def read_json():
    
    with open(Path(home+'config.json')) as json_data_file:
        data = json.load(json_data_file)
    
    return data

def write_json(data, h=home):
    
    with open(Path(home+'config.json'), 'w') as outfile:
        json.dump(data, outfile)
