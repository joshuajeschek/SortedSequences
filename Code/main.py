from abTree import *
from random import randrange


def main():
    tree = ABTree()
    for x in range(0, 200, 1):
        i = randrange(0, 200, 1)
        print('>>> Inserting ', i)
        tree.insert(i, x)
    x = randrange(0, 200, 1)
    for x in range(0, 200, 1):
        print(f'Looking for Leaf with key {x}')
        target = tree.locate(x)
        print(f'Found: {target}')
        print(vars(target))
        print(f'Deleting Leaf with key {x}')
        tree.remove(x)
        target = tree.locate(x)
        print(f'Found: {target}')
        print(vars(target))


if __name__ == '__main__':
    main()
