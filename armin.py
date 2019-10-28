import os
import csv
import sys
from itertools import combinations
from itertools import permutations
import math

import pandas as pd


def main():
    args = sys.argv[1:]
    if not args:
        print("improper args")
        print("python armin.py *input* *output* *sp* *conf*")
        sys.exit(1)
    file_in = args[0]
    file_out = args[1]
    min_support_percentage = float(args[2])
    min_confidence = float(args[3])

    # need pseudo - header with all of the items

    if os.path.isfile(os.path.join(os.getcwd(), file_in)):
        f = os.path.join(os.getcwd(), file_in)
        items = set(())
        basket = []
        lookup = []

        # runtime

        if os.path.isfile(os.path.join(os.getcwd(), file_in)):
            with open(file_in, 'r') as csvfile:
                reader = csv.reader(csvfile, delimiter='\n', quotechar='|')
                for row in reader:
                    r = ','.join(row).split(',')
                    index = r[0]
                    r = r[1:]
                    d = [i.strip() for i in r]
                    lookup.append(index)
                    r = {i.strip() for i in r}
                    if d is None:
                        d = []
                    basket.append(d)
                    items = items.union(r)

        # items is set of unique item names
        # basket is a list of lists - baskets for each transaction

        items = list(items)
        items.sort()
        cfi = []
        support_index = []
        # items.insert(0, "trans_id")

        for i in range(len(items) + 1):
            print(cfi)
            comb = combinations(items, i + 1)
            # remove shit from combinations
            # i guess that happens with -items
            for j in comb:
                j = set(j)
                print(j)
                count = 0
                for a in basket:
                    temp = set(a)
                    if j.issubset(temp):
                        count += 1
                print(count/len(basket))
                support = count/len(basket)
                if support >= min_support_percentage:
                    if len(j) == 1:
                        j = list(j)
                        cfi.append(list((j[0])))
                        support_index.append(support)
                    else:
                        j = list(j)
                        j.sort()
                        cfi.append(j)
                        support_index.append(support)
                elif count/len(basket) < min_support_percentage and len(j) == 1:
                    j = list(j)
                    items.remove(j[0])
        print(cfi)
        print(support_index)

        with open('test_out.csv', "w", newline="") as f:
            for i in range(len(cfi)):
                row = csv.writer(f)
                temp = cfi[i]
                temp.insert(0, 'S')
                temp.insert(1, '%.4f' % support_index[i])
                row.writerow(temp)

        #
        # df = pd.read_csv(f, names=items, error_bad_lines=False, warn_bad_lines=False, skipinitialspace=True, header=None)
        # df = pd.DataFrame(df)
        # df.fillna(0, inplace=True)
        # print(df.head(10))

        # df.to_csv(file_out)


if __name__ == '__main__':
    main()
