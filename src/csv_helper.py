import os
import csv
import logging

from .constants import CSVS

logger = logging.getLogger(__name__)


def csv_to_dicts(file_path):
    with open(file_path) as f:
        return [{ k: v for k, v in row.items() } for row in csv.DictReader(f, skipinitialspace=True)]

def csv_to_lists(file_path):
    result = []
    with open(file_path, 'r', errors='ignore') as f:
        lines = f.readlines()
        for line in lines:
            result.append(line.split(','))
    return result


def get_matches_csvs(year):
    file_names = ['atp_matches_', 'atp_matches_qual_chall_', 'atp_matches_futures_']
    return [os.path.join(CSVS, file_name + str(year) + '.csv') for file_name in file_names]