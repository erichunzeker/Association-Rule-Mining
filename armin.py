import os
import csv
import pandas as pd

file_in = input('Enter name of input file: ')


if os.path.isfile(os.path.join(os.getcwd(), file_in)):
    f = os.path.join(os.getcwd(), file_in)
    df = pd.read_csv(f, error_bad_lines=False, warn_bad_lines=False, skipinitialspace=True)
    print(df.head())

# if os.path.isfile(os.path.join(os.getcwd(), file_in)):
#     # use csv lib to convert to python dictreader
#     file = csv.DictReader(open(file_in))
#     # open csv, set dilimter to new line, read and print line by line for part 5
#     with open(file_in, 'r') as csvfile:
#         reader = csv.reader(csvfile, delimiter='\n', quotechar='|')
#         for row in reader:
#             r = ','.join(row).split(',')
#             r = [i.strip() for i in r]
#             print(r)
