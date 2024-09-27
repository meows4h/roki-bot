import csv
import re

def str_clean(str):
    sanitized = re.sub(r'[^\x00-\x7F]+', '', str)
    sanitized = sanitized.replace('\n', '')
    return sanitized

csv_file = input('csv name: ')
csv_file += '.csv'

username = input('user: ')

fields = ['input','output']
export = []

move_check = 0

with open(csv_file, 'r', encoding='utf-8') as csvfile:

    csvreader = csv.reader(csvfile)
    
    input_cache = ''
    output_cache = ''

    for row in csvreader:

        if username in row:

            if move_check == 2:
                input_cache = str_clean(input_cache)
                output_cache = str_clean(output_cache)
                export_cache = [input_cache, output_cache]
                export.append(export_cache)
                print(f'"{export_cache}" added.')
                input_cache = ''
                output_cache = ''

            move_check = 1
            input_cache += row[3] + ' '

        elif 'v.cat' in row:

            move_check = 2
            output_cache = row[3] + ' '


with open('output.csv', 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(fields)
    csvwriter.writerows(export)