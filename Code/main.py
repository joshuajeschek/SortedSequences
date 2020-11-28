from abTree import *
from random import randrange


def main():
    tree_1 = ABTree()
    for x in range(0, 30, 1):
        i = randrange(120, 200, 1)
        # print('>>> Inserting ', i)
        tree_1.insert(i, x)

    print(f'tree_1: {tree_1.height}')

    result = tree_1.getHeight()
    print(result)

    tree_2 = ABTree()
    for x in range(0, 60, 1):
        i = randrange(0, 120, 1)
        # print('>>> Inserting ', i)
        tree_2.insert(i, x)

    print(f'tree_2: {tree_2.height}')

    result = tree_2.getHeight()
    print(result)


if __name__ == '__main__':
    main()
