import csv


def csv_to_dicts(file_path):
    reader = csv.DictReader(open(file_path, 'rb'))
    # to: feels like no sence in this line
    return [line for line in reader]

def csv_to_lists(file_path):
    result = []
    with open(file_path) as f:
        lines = f.readlines()
        for line in lines:
            result.append(line.split(','))