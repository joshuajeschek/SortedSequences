from dll import *
from math import floor, ceil

A = 2
B = 4


class Node:

    """A Node of a tree, containing splitters, children and degree"""

    def __init__(self, children, splitters=[]):
        self.c = [None]                 # c[0]
        if isinstance(children, list):  # multiple children provided as a list
            self.c = self.c + children
        else:
            self.c.append(children)
        self.s = [float('-inf')]        # leftmost splitter (s[0])
        if isinstance(splitters, list):
            for item in splitters:
                self.s.append(item)
        else:
            self.s.append(splitters)
        self.d = len(self.c) - 1        # account for c[0]
        self.s.append(float('inf'))     # rightmost splitter (s[d])

    def locateLocally(self, key):
        '''calculates the index of the child containing the given key'''

        i = 1
        while i <= (self.d):
            if key <= self.s[i]:
                return i
            i += 1

    def getMax(self):
        '''returns the last node in the tree, without using the list'''

        if isinstance(self.c[self.d], Leaf):
            return self.c[self.d]
        else:
            return self.c[self.d].getMax()

    def locateRec(self, key, height):
        '''finds the element with the given key, if it exists.
        If not: returns the next element'''

        i = self.locateLocally(key)
        if height == 1:     # bottom of tree reached
            if self.c[i].key >= key:
                return self.c[i]
            else:
                # -> next element (leftmost in next node)
                return self.c[i].succ
        else:
            # descend to lower level in the tree
            return self.c[i].locateRec(key, (height - 1))

    def insertRec(self, key, value, h):
        '''inserts an element with the given key
        and value at the correct position'''

        i = self.locateLocally(key)
        if h == 1:     # bottom of tree reached
            if self.c[i].key == key:    # replace value, element exists
                self.c[i].value = value
                return None, None       # tree does not need to change
            else:
                if self.c[i].key > key:     # found successor of new element
                    k, t = key, self.c[i].insertBefore(key, value)
                else:   # found predecessor of new element
                    k, t = self.c[i].key, self.c[i].insertAfter(key, value)
                    self.c[i], t = t, self.c[i]
        else:
            k, t = self.c[i].insertRec(key, value, (h - 1))
            if t is None:
                return None, None

        # new splitter list, children list and degree calculation:
        s1 = [float('-inf')]
        for x in range(1, i, 1):
            s1.append(self.s[x])
        s1.append(k)
        for x in range(i, self.d + 1, 1):
            s1.append(self.s[x])

        c1 = [None]
        for x in range(1, i, 1):
            c1.append(self.c[x])
        c1.append(t)
        for x in range(i, self.d + 1, 1):
            c1.append(self.c[x])

        d1 = len(c1) - 1    # account for c[0]

        if d1 <= B:     # still space in node to accomodate all children
            self.s, self.c, self.d = s1, c1, (self.d + 1)
            return None, None   # node above does not change
        else:           # node needs to be split
            self.d = floor((B + 1) / 2)

            self.s = s1[(B + 2 - self.d):]
            self.s.insert(0, float('-inf'))

            self.c = c1[(B + 2 - self.d):]
            self.c.insert(0, None)

            # return new node and splitter to
            # next level of recursion (node above)
            # -> new child can be created there
            return s1[B + 1 - self.d], Node(
                c1[1:(B + 1 - self.d + 1)], s1[1:(B - self.d + 1)])

    def removeLocally(self, i):
        '''removes a child from a node'''

        self.c[i:self.d] = self.c[(i + 1):(self.d + 1)]
        self.s[i:(self.d - 1)] = self.s[(i + 1):self.d]
        self.d = len(self.c) - 1

    def removeRec(self, key, h):
        '''removes an element from the sequence'''
        i = self.locateLocally(key)
        if h == 1:      # bottom of tree reached
            if self.c[i].key == key:
                self.c[i].remove()      # remove Leaf from list
                self.removeLocally(i)   # remove from node
        else:
            self.c[i].removeRec(key, (h - 1))
            if self.c[i].d < A:  # node needs to be balanced
                if i == self.d:
                    i -= 1

                    # constructing new node from neighbor and current node
                    s1 = []
                    for splitter in self.c[i].s:
                        s1.append(splitter)
                    s1.append(self.s[i])
                    for splitter in self.c[i + 1].s:
                        splitter != float('-inf') and s1.append(splitter)

                    c1 = []
                    for child in self.c[i].c:
                        c1.append(child)
                    for child in self.c[i + 1].c:
                        child is not None and c1.append(child)

                    d1 = len(c1) - 1    # account for c[o]

                    if d1 <= B:     # new node is legal
                        self.c[i + 1].s = s1
                        self.c[i + 1].c = c1
                        self.c[i + 1].d = d1

                    else:           # new node exceeds B, needs to be split
                        m = ceil(d1 / 2)

                        self.c[i].s = s1[0:m]
                        self.c[i].c = c1[0:(m + 1)]
                        self.c[i].d = m

                        self.c[i + 1].s = s1[(m + 1):d1]
                        self.c[i + 1].c = c1[(m + 1):(d1 + 1)]
                        self.c[i + 1].d = d1 - m

                        self.s[i] = s1[m]

    def mergeRec(self, lvl, root, splitter, l_r):
        '''merging of two trees, represented as two roots.
        can be don on the left side of  current node (l_r='l')
        or on the right side (l_r='r')
        lvl describes height difference,
        splitter is maximum of the tree on the left side'''

        if l_r == 'l':  # descend on left side
            i = 1
        else:           # descend on right side
            i = self.d
        if lvl == 0:    # reached point where tree is attached
            root.s[-1] = splitter
            k, t = root.s[1:], root.c[1:]

        else:
            k, t = self.c[i].mergeRec((lvl - 1), root, splitter, l_r)
            if t is None:
                return None, None

        # create new node
        s1 = [float('-inf')]
        for x in range(1, i, 1):
            s1.append(self.s[x])
        if isinstance(k, list):     # can be single splitter or list
            for element in k:
                s1.append(element)
        else:
            s1.append(k)
        for x in range(i, self.d + 1, 1):
            s1.append(self.s[x])

        c1 = [None]
        for x in range(1, i, 1):
            c1.append(self.c[x])
        if isinstance(t, list):     # cam be single child or list
            for child in t:
                c1.append(child)
        else:
            c1.append(t)
        for x in range(i, self.d + 1, 1):
            c1.append(self.c[x])

        d1 = len(c1) - 1    # account for c[0]

        if d1 <= B:     # still room for everything
            self.s, self.c, self.d = s1, c1, d1
            return None, None   # nothing changed for parent
        else:           # splitting needed
            self.d = floor(d1 / 2)

            self.s = s1[(-self.d):]
            self.s.insert(0, float('-inf'))

            self.c = c1[(-self.d):]
            self.c.insert(0, None)

            # return new Node with splitter for parent
            return s1[B + 1 - self.d], Node(
                c1[1:(-self.d)], s1[1:(-self.d - 1)])

    def splitRec(self, key, height, head_r, first):
        '''splitting a root node into two new trees'''

        i = self.locateLocally(key)
        if height == 1:
            # splitting the list
            head_l = Leaf(float('inf'), self.c[i].prev, first)
            self.c[i].prev.succ = head_l
            first.prev = head_l

            self.c[i].prev = head_r
            head_r.succ = self.c[i]
            # two linked lists

            # creating new trees
            subtree_l, subtree_r = ABTree(), ABTree()

            # attaching dummy element to left tree
            subtree_l.root = Node(self.c[1:i], self.s[1:(i - 1)])
            subtree_l.list.head = head_l
            subtree_l.height = 1
            dummyroot = Node(head_l)
            if subtree_l.root.d > 0:    # left tree contains elements
                k, t = subtree_l.root.mergeRec(0, dummyroot,
                                               subtree_l.root.c[-1].key, 'r')
                if t is not None:
                    subtree_l.root = Node([t, subtree_l.root], k)
                    subtree_l.height += 1
            else:   # left tree only contains root
                subtree_l.root = dummyroot

            # managing right tree
            subtree_r.root = Node(self.c[i:], self.s[i:-1])
            subtree_r.list.head = head_r
            subtree_r.height = 1

            return subtree_l, subtree_r

        else:
            subtree_l, subtree_r = self.c[i].splitRec(key, (height - 1),
                                                      head_r, first)

        # attaching node_l to rest of subtree_l
        node_l = Node(self.c[1:i], self.s[1:(i - 1)])
        if node_l.d > 0:
            k, t = node_l.mergeRec(height - subtree_l.height,
                                   subtree_l.root, node_l.getMax().key, 'l')
            if t is not None:
                subtree_l.root = Node([t, node_l], k)
                subtree_l.height = height + 1
            else:
                subtree_l.root = node_l
                subtree_l.height = height

        # attaching node_r to rest of subtree_r
        node_r = Node(self.c[i:], self.s[i:-1])
        if node_r.d > 0:
            k, t = node_r.mergeRec(height - subtree_r.height,
                                   subtree_r.root, subtree_l.last().key, 'r')
            if t is not None:
                subtree_r.root = Node([t, node_r], k)
                subtree_r.height = height + 1
            else:
                subtree_r.root = node_r
                subtree_r.height = height

        return subtree_l, subtree_r


class ABTree:
    """An (a,b)-Tree, represented as a root.
    Also contains a list/its head and the height"""

    def __init__(self):
        self.list = DoublyLinkedList()
        self.root = Node([self.list.head])
        self.height = 1

    def locate(self, key):
        '''locates an element with the given key'''

        return self.root.locateRec(key, self.height)

    def insert(self, key, value):
        '''inserts an element with the given key'''

        k, t = self.root.insertRec(key, value, self.height)
        if t is not None:   # root node needs to be split
            self.root = Node([t, self.root], k)
            self.height += 1

    def remove(self, key):
        '''removes an element with the given key, if it exists'''

        self.root.removeRec(key, self.height)
        if self.root == 1 and self.height > 1:  # height will decrease
            old = self.root
            self.root = old.c[1]
            del old
            self.height -= 1

    def listAll(self):
        '''lists all elements of the underlying list on the command line'''
        self.list.listAll()

    def count(self):
        '''returns number of elements in the list'''
        return self.list.count()

    def first(self):
        '''returns first element in the list
        returns None, if tree is empty!'''
        return self.list.first()

    def last(self):
        '''returns last element in the list
        returns None, if tree is empty!'''
        return self.list.last()

    def isEmpty(self):
        '''returns True or False,
        wether tree contains elements or not'''
        return self.list.isEmpty()

    def locateRange(self, start, end):
        '''returns a list of elements in the given range'''

        current = self.locate(start)
        result = []
        while current.key <= end:
            result.append(current)
            current = current.succ
        return result

    def split(self, key):
        '''splits tree at the given key,
        returns two new trees'''

        if self.isEmpty():  # return two empty trees
            return self, ABTree()
        elif self.first().key >= key:
            # key is smaller than first element in tree
            # return empty tree and self
            return ABTree(), self
        elif self.last().key < key:
            # key is bigger than last element in tree
            # return self and empty tree
            return self, ABTree()

        tree_l, tree_r = self.root.splitRec(
            key, self.height, self.list.head, self.first())
        return tree_l, tree_r

# =================================================
# MERGE ===========================================
# =================================================


def mergeTrees(tree_1, tree_2):
    '''merges two trees and returns one'''

    if tree_1.isEmpty():
        return tree_2
    elif tree_2.isEmpty():
        return tree_1
    elif tree_1.isEmpty() and tree_2.isEmpty():
        return tree_1

    if tree_1.last().key >= tree_2.first().key:     # overlapping
        if tree_2.last().key >= tree_1.first().key:
            # checking if trees could be switched and then merged
            return None
        else:
            tree_1, tree_2 = tree_2, tree_1     # switch trees

    # merge the underlying lists
    tree_1.last().succ = tree_2.first()
    tree_2.first().prev = tree_1.last()

    tree_1.first().prev = tree_2.list.head
    tree_2.list.head.succ = tree_1.first()

    # merge smaller tree to higher tree
    if tree_1.height >= tree_2.height:
        tree_1.list = tree_2.list
        k, t = tree_1.root.mergeRec((tree_1.height - tree_2.height),
                                    tree_2.root,
                                    tree_1.last().key,
                                    'r')
        if t is not None:   # root needs to be split
            tree_1.root = Node([t, tree_1.root], k)
            tree_1.height += 1
        return tree_1

    else:
        k, t = tree_2.root.mergeRec((tree_2.height - tree_1.height),
                                    tree_1.root,
                                    tree_1.last().key,
                                    'l')
        if t is not None:   # root needsd to be split
            tree_2.root = Node([t, tree_2.root], k)
            tree_2.height += 1
        return tree_2
