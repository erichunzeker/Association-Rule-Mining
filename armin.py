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
        items = set(())
        basket = []
        lookup = []
        cfi = []
        support_index = []

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

        # number of unique items
        for i in range(len(items) + 1):

            # comb is every combination of possible subsets
            comb = combinations(items, i + 1)

            # number of unique items * length of subset
            for j in comb:
                # do something to make j smaller by removing impossible subsets
                j = set(j)
                count = 0

                # number of transactions
                for a in basket:
                    temp = set(a)
                    # if current combination/subset of unique items is in current transaction
                    if j.issubset(temp):
                        count += 1

                support = count/len(basket)

                if support >= min_support_percentage:
                    # make accepted subset into list, sort it, and include it in cfi
                    j = list(j)
                    j.sort()
                    cfi.append(j)
                    # include the support percentage that it got through with in an adjacent array
                    support_index.append(support)

                # if it's a single item and it's not in cfi, don't allow it in further combinations
                elif len(j) == 1 and support < min_support_percentage:
                    j = list(j)
                    items.remove(j[0])

        with open(file_out, "w", newline="") as f:
            for i in range(len(cfi)):
                row = csv.writer(f)
                temp = cfi[i]
                temp.insert(0, 'S')
                temp.insert(1, '%.4f' % support_index[i])
                row.writerow(temp)


if __name__ == '__main__':
    main()
