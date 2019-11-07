import os
import csv
import sys
from itertools import combinations


def main():
    args = sys.argv[1:]
    if not args or len(args) < 4:
        print("improper args - use `python armin.py *input* *output* *sp* *conf*`")
        sys.exit(1)

    min_support_percentage = float(args[2])
    min_confidence = float(args[3])

    items = set(())
    basket = []
    vfi = []
    support_index = []

    # go through input csv and gather unique items and create a nested list of transactions
    # items is set of unique item names; basket is a list of lists - baskets for each transaction
    if os.path.isfile(os.path.join(os.getcwd(), args[0])):
        with open(args[0], 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter='\n', quotechar='|')
            for row in reader:
                r = ','.join(row).split(',')[1:]
                d = [i.strip() for i in r]
                r = {i.strip() for i in r}
                basket.append(d)
                items = items.union(r)
    items = list(items)
    items.sort()

    # number of unique items
    for i in range(len(items) + 1):
        # comb is every combination of possible subsets
        comb = combinations(items, i + 1)

        # runtime: number of unique items * length of subset
        for c in comb:
            c = set(c)
            count = 0
            # runtime: number of transactions
            for a in basket:
                a = set(a)
                # if current combination/subset of unique items is in current transaction
                if c.issubset(a):
                    count += 1

            support = count / len(basket)

            if support >= min_support_percentage:
                # make accepted subset into list, sort it, and include it in vfi
                c = list(c)
                c.sort()
                vfi.append(c)
                # include the support percentage that it got through with in an adjacent array
                support_index.append(support)

            # if it's a single item and it's not in vfi, don't allow it in further combinations
            elif len(c) == 1:
                c = list(c)
                items.remove(c[0])

    with open(args[1], "w", newline="") as f:
        for i in range(len(vfi)):
            row = csv.writer(f)
            line = vfi[i]
            line.insert(0, 'S')
            line.insert(1, '%.4f' % support_index[i])
            row.writerow(line)

        # subsets (get all subsets that made the min_support cut)
        ss = vfi.copy()
        ss = [x[2:] for x in ss]

        # make lookup table of subset & support_percent (key: str vrsn of subset, val: support_percent)
        unions = vfi.copy()
        unions = {(str(x[2:])): x[1] for x in unions}

        # only two side of confidence (a => b), so only make combinations size 2
        for pair in combinations(ss, 2):
            pair = list(pair)
            a = set(pair[0])
            b = set(pair[1])

            u = a.union(b)
            u = list(u)
            u.sort()

            # index unions with the union of the two sides, needed for algorithm's equation
            if str(u) in unions:
                union_support_percent = float(unions[str(u)])
                first = list(a)
                first.sort()

                second = list(b)
                second.sort()

                if len(a.intersection(b)) == 0:
                    row = csv.writer(f, quoting=csv.QUOTE_NONE, quotechar=None, escapechar='\\')

                    first_support_percent = float(unions[str(first)])
                    flipped_support_percent = float(unions[str(second)])

                    conf = union_support_percent / first_support_percent
                    flipped_conf = union_support_percent / flipped_support_percent

                    if conf >= min_confidence:
                        row.writerow(['R'] + [str('%.4f' % union_support_percent)] +
                                     [str('%.4f' % conf)] + first + ['\'=>\''] + second)

                    if flipped_conf >= min_confidence:
                        row.writerow(['R'] + [str('%.4f' % union_support_percent)] +
                                     [str('%.4f' % flipped_conf)] + second + ['\'=>\''] + first)


if __name__ == '__main__':
    main()
