# Gareth's Interval Checker
# September 2020 v.02

import csv
import os
from datetime import datetime, timedelta
from datetimerange import DateTimeRange
from matplotlib import pyplot as plt
from tqdm import tqdm


def file_selector(files):
    count = 1
    options = {}
    print('List of available .csv files:')
    for file in files:
        if file[-4:] == '.csv':
            print(count, ':', file)
            options.update({count: file})
            count += 1
    selection = input('Type the number for the file you want to use: \n')
    datafile = options[int(selection)]
    return datafile


def type_creator(file_name):
    types_list = []
    with open(file_name, mode='r') as csv_file:
        items_to_check = csv.DictReader(csv_file)
        for item in tqdm(items_to_check):
            if item['type'] in types_list:
                continue
            else:
                types_list.append(item['type'])
    return types_list


def time_range(start, end, delta):
    current = start
    intervals = []
    while current < end:
        endtime = current + timedelta(minutes=delta - 1, seconds=59)
        intervals.append(DateTimeRange(current, endtime))
        current = current + timedelta(minutes=delta)
    return intervals


def data_set(start, end, delta, groups):
    result = []
    period = time_range(start, end, delta)
    count = 0
    for item in period:
        data = {}
        data.update({'Time Period': item})
        result.append(data)
        count += 1
    for x in result:
        for y in groups:
            x.update({y: 0})
    return result


def axis_generator(start, end, delta):
    axis_to_generate = time_range(start, end, delta)
    axis_labels = []
    for timerange in axis_to_generate:
        timerange.start_time_format = "%d/%m %H:%M"
        axis_labels.append(timerange.get_start_time_str())
    return axis_labels


def checker(data_file, start, end, intervals, types2):
    num_lines = sum(1 for line in open(datafile,'r'))
    with open(data_file, mode='r') as csv_file:
        items_to_check = csv.DictReader(csv_file)
        period_to_check = data_set(start, end, intervals, types2)
        for item in tqdm(items_to_check, total=num_lines):
            start_item = datetime.strptime(item['start'], '%d/%m/%Y %H:%M:%S')
            end_item = datetime.strptime(item['end'], '%d/%m/%Y %H:%M:%S')
            for period in period_to_check:
                period_start = period['Time Period'].start_datetime
                period_end = period['Time Period'].end_datetime
                if start_item in period['Time Period']:
                    type_count = period[item['type']]
                    type_count += 1
                    period.update({item['type']: type_count})
                elif end_item in period['Time Period']:
                    type_count = period[item['type']]
                    type_count += 1
                    period.update({item['type']: type_count})
                elif start_item < period_start and end_item > period_end:
                    type_count = period[item['type']]
                    type_count += 1
                    period.update({item['type']: type_count})
        return period_to_check


def csv_writer(output_file_name, data_export):
    types.insert(0, 'Time Period')
    columns = types
    with open(output_file_name + '.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=columns)
        writer.writeheader()
        for data in data_export:
            writer.writerow(data)


directory = os.getcwd()
files = os.listdir(directory)
start_time = datetime.strptime(input('Enter start of time period (DD/MM/YYYY HH:MM:SS): \n '), '%d/%m/%Y %H:%M:%S')
end_time = datetime.strptime(input('Enter end of time period (DD/MM/YYYY HH:MM:SS): \n '), '%d/%m/%Y %H:%M:%S')
interval = int(input('Enter the interval in minutes: \n'))
datafile = file_selector(files)
output_file = str(input('Enter the full name (excluding file type) of the file you want creating: \n'))
types = type_creator(datafile)
result = checker(datafile, start_time, end_time, interval, types)
csv_writer(output_file, result)

