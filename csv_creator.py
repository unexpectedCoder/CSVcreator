"""
This module provides capabilities for transfer data from TXT file (source) to CSV file (target).
"""


import csv
import numpy as np


def from_txt(fsrc, ftarg, head=None, sep=' '):
    """
    Reads data from TXT file and then writes it to CSV file.
    TXT may include header row (in that case 'head' arg is 'None')
    or not (in that case 'head' arg is a list (tuple) of text header's info).
    :param fsrc: source TXT file's path (without extension)
    :type fsrc: str
    :param ftarg: target CSV file's path (without extension)
    :param head: list of header's values
    :type head: list
    :param sep: data separator in TXT file
    :type sep: str
    :return: source and target files' paths
    """
    if '.' not in fsrc:
        fsrc += '.txt'
    if '.' not in ftarg:
        ftarg += '.csv'
    if check_file_exist(fsrc, fatal=True) is None:
        exit(-1)
    # Checking
    choice = ''
    if check_file_exist(ftarg) is False:     # i.e. file may be created
        if input(f"File '{ftarg}' doesn't exist.\nDo you want to create it? (+/-): ") == '+':
            open(ftarg, 'w').close()
    else:
        print(f"WARNING: file '{ftarg}' is existing.")
        choice = input("Choose action with it: 'w' - rewrite file, 'a' - add to end: ")
    # Run
    fieldnames, data = read_txt_data(fsrc, head=head, sep=sep)
    write_csv(ftarg, fieldnames, data, mode=choice)
    return fsrc, ftarg


def check_file_exist(path, fatal=False):
    """
    Checks existing of file with input folder.
    :param path: file's path
    :type path: str
    :param fatal: True if non-existing file is a fatal error for program
    :type fatal: bool
    :return: True - if file exists, 0 - if file doesn't exist but may be created, False - in other cases
    """
    try:
        f = open(path, 'r')
    except FileNotFoundError:
        if fatal:
            return None
        return False
    else:
        f.close()
    return True


def read_txt_data(path, head=None, sep=' '):
    """
    Reads header (if 'head' is None) and data from TXT file.
    :param path: TXT file's path
    :type path: str
    :param head: list of header's fields
    :type head: list
    :param sep: data separator
    :type sep: str
    :return: fieldnames, data
    """
    with open(path, 'r') as src:
        fieldnames = src.readline().rstrip().split(sep) if head is None else head.copy()
        data_arr = np.array([line.rstrip().split(' ') for line in src])
        for i, d in enumerate(data_arr):
            if len(d) != len(fieldnames):
                print(f"Error: length of {i + 2 if head is None else i + 1} row is not equal to length of header!")
                raise ValueError
        data = {key: data_arr[:, col].tolist() for col, key in enumerate(fieldnames)}
    return fieldnames, data


def write_csv(path: str, fieldnames: list, data: dict, mode='w'):
    """
    Fills CSV file using input fieldnames and data.
    :param path: CSV target file's path
    :param fieldnames: data fieldnames
    :param data: input data
    :param mode: file opening mode ('w' or 'a')
    :type mode: str
    :return: nothing
    """
    if data == {} or data == [] or data is None:
        print("Error: data argument has invalid value!")
        raise ValueError
    if mode != 'w' and mode != 'a':
        print("Error: invalid file opening mode! Expected 'w' or 'a'...")
        raise ValueError
    with open(path, mode, newline='') as f:
        writer = csv.DictWriter(f, fieldnames)
        if mode == 'w':
            writer.writeheader()
        writer.writerow(data)


def read_csv(path: str, show: bool = False):
    """
    Reads and shows CSV file's content.
    :param path: CSV file's path
    :param show: should be the CSV content to be shown?
    :return: data from CSV (OrderedDict)
    """
    with open(path + '.csv', 'r', newline='') as f:
        reader = csv.DictReader(f)
        if show:
            for row in reader:
                print("CSV file content:", row)
    return reader
