from abTree import *
from random import randrange


def main():
    tree = ABTree()
    for x in range(0, 100, 1):
        i = randrange(0, 1000, 1)
        # print('>>> Inserting ', i)
        tree.insert(i, x)

    targets = [(100, 42), (200, 42), (300, 42), (400, 42),
               (500, 42), (600, 42), (700, 42), (800, 42), (900, 42)]

    tree.bulkInsert(targets)

    tree.listAll()

    # tree_1, tree_2 = tree.split(500)
#
    # print('tree_1:')
    # tree_1.listAll()
#
    # print('tree_2:')
    # tree_2.listAll()


if __name__ == '__main__':
    while True:
        main()
