import os
import csv
import sys

import pandas as pd


def main():
    args = sys.argv[1:]
    if not args:
        print("improper args")
        print("python armin.py *input* *output* *sp* *conf*")
        sys.exit(1)
    file_in = args[0]
    file_out = args[1]

    # need pseudo - header with all of the items

    if os.path.isfile(os.path.join(os.getcwd(), file_in)):
        f = os.path.join(os.getcwd(), file_in)
        df = pd.read_csv(f, error_bad_lines=False, warn_bad_lines=False, skipinitialspace=True, header=None)
        df = pd.DataFrame(df, columns=['transaction'])
        print(df.head())

        df.to_csv(file_out)


if __name__ == '__main__':
    main()
