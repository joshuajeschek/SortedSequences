from abTree import *
from random import randrange


def main():
    tree = ABTree()
    for x in range(0, 1000, 1):
        i = randrange(0, 10000, 1)
        # print('>>> Inserting ', i)
        tree.insert(i, x)

    print('tree:')
    tree.listAll()

    tree_l, tree_r = tree.split(5000)

    print('tree_l:')
    tree_l.listAll()

    print('tree_r:')
    tree_r.listAll()

    i = randrange(5000, 10000, 1)
    print(f'tree_r({i}):')
    result = tree_r.locate(i)
    print(vars(result))

    i = randrange(0, 50, 1)
    print(f'tree_l({i}):')
    result = tree_l.locate(i)
    print(vars(result))

    del tree, tree_l, tree_r


if __name__ == '__main__':
    i = 1
    while True:
        print(f'Durchlauf: {i}')
        main()
        i += 1
