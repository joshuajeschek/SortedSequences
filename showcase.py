from abTree import *
from random import randint


def main():
    size_1 = int(input('Specify size of Tree 1: '))
    print(
        f'Creating random tree with maximum size {size_1} with random keys from 0 to {size_1*10}.')
    print('The value will indicate, at which point it was inserted.')

    tree_1 = ABTree()

    for value in range(0, size_1):
        key = randint(0, size_1 * 10)
        tree_1.insert(key, value)

    input('Press enter to list all elements in the tree...')
    tree_1.listAll()

    print('\n--- locate() ---')
    while True:
        searchkey = input(
            'Specify a key for which to search for (or press enter to continue): ')
        if searchkey == '':
            break
        else:
            target = tree_1.locate(int(searchkey))
            print('Found the following leaf (printing all attributes):')
            print(vars(target))

    print('\n--- insert() ---')
    while True:
        insertkey = input(
            'Specify a key for an element to insert it (or press enter to continue): ')
        if insertkey == '':
            break
        insertvalue = int(input('Specify a value for the element: '))
        tree_1.insert(int(insertkey), insertvalue)
        input('Press enter to see the current contents of the tree...')
        tree_1.listAll()

    print('\n--- remove() ---')
    while True:
        removekey = input(
            'Specify a key for an element to delete it (or press enter to continue): ')
        if removekey == '':
            break
        else:
            tree_1.remove(int(removekey))
            input('Press enter to see the current contents of the tree...')
            tree_1.listAll()

    max_1 = tree_1.last()
    if max_1 is None:
        max_1 = 0
    else:
        max_1 = max_1.key

    print('\n--- merge() ---')
    size_2 = int(input('Specify a size for the second tree: '))
    print(
        f'Creating a second random tree with maximum size {size_2} with random keys between {max_1 + 1} and {(size_2 * 10) + max_1 + 1}')
    print('The value will indicate, at which point it was inserted.')

    tree_2 = ABTree()

    for value in range(0, size_2):
        key = randint(max_1 + 1, (size_2 * 10) + max_1 + 1)
        tree_2.insert(key, value)

    input('Press enter to list all elements in the new tree...')
    tree_2.listAll()

    input('\nPress enter to merge the both trees and see the new tree...')
    mergedTree = mergeTrees(tree_1, tree_2)
    mergedTree.listAll()

    print('\n--- split() ---')
    splitkey = int(input('Specify a key to split the tree at: '))

    input('Press enter to tree 1:')
    tree_1, tree_2 = mergedTree.split(splitkey)

    print('Tree 1:')
    tree_1.listAll()

    input('Press enter to tree 2:')

    print('Tree 2:')
    tree_2.listAll()


if __name__ == '__main__':
    main()
