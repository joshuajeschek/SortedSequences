from abTree import *
import csv
from random import randrange
import time
from datetime import datetime

def main():

    x = 0
    while x < 5:
        x += 1
        i = 300000

        tree = ABTree()

        with open(f'benchmark-30000-{x}.csv', mode='w', newline='') as csv_file:
            print(f'opened file ({x})')
            fieldnames = ['n', 'locate', 'h', 'timestamp']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            print('wrote header')

            j = 0
            while j <= i:
                print(j, end='\r')
                r = randrange(0, i * 100)

                tree.insert(r, 'foo')

                start = time.perf_counter()
                res = tree.locate(r)
                end = time.perf_counter()

                writer.writerow({'n': tree.list.count(),
                                 'locate': end - start,
                                 'h': tree.height,
                                 'timestamp': datetime.now()})
                j += 1
        del tree


if __name__ == '__main__':
    main()
