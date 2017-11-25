from datetime import datetime


def years_from_timestamp(timestamp):
    start_date = datetime.fromtimestamp(timestamp)
    end_date = datetime.now()
    years = start_date.year - end_date.year
    if end_date.month < start_date.month or (end_date.month == start_date.month and end_date.day < start_date.day):
        years -= 1
    return years