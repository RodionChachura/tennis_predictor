import os
import csv

from .constants import CSVS


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


def get_matches_csvs(year):
    file_names = ['atp_matches_', 'atp_matches_quall_chall_', 'atp_matches_futures_']
    return [os.path.join(CSVS, file_name + str(year) + '.scv') for file_name in file_names]