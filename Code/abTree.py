from dll import *
from math import floor, ceil

A = 2
B = 4


class Node:
    """A Node of a tree, containing splitters, children and degree"""

    def __init__(self, children, splitters=[]):
        self.c = [None] + children
        self.s = [float('-inf')]
        if isinstance(splitters, list):
            for item in splitters:
                self.s.append(item)
        else:
            self.s.append(splitters)
        self.d = len(self.c) - 1    # account for c[0]
        self.s.append(float('inf'))

    def locateLocally(self, key):
        i = 1
        while i <= (self.d):
            if key <= self.s[i]:
                return i
            i += 1
        return

    def locateRec(self, key, height):
        i = self.locateLocally(key)
        if height == 1:
            if self.c[i].key >= key:
                return self.c[i]
            else:
                return self.c[i].succ
        else:
            return self.c[i].locateRec(key, (height - 1))

    def insertRec(self, key, value, h):   # deleted argument l
        i = self.locateLocally(key)
        if h == 1:
            if self.c[i].key == key:
                self.c[i].value = value
                return None, None
            else:
                if self.c[i].key > key:
                    k, t = key, self.c[i].insertBefore(key, value)
                else:
                    k, t = self.c[i].key, self.c[i].insertAfter(key, value)
                    self.c[i], t = t, self.c[i]
        else:
            k, t = self.c[i].insertRec(key, value, (h - 1))
            if t is None:
                return None, None

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

        d1 = len(c1) - 1

        if d1 <= B:
            self.s, self.c, self.d = s1, c1, (self.d + 1)
            return None, None
        else:
            self.d = floor((B + 1) / 2)

            self.s = s1[(B + 2 - self.d):]
            self.s.insert(0, float('-inf'))

            self.c = c1[(B + 2 - self.d):]
            self.c.insert(0, None)

            return s1[B + 1 - self.d], Node(
                c1[1:(B + 1 - self.d + 1)], s1[1:(B - self.d + 1)])

    def removeLocally(self, i):
        self.c[i:self.d] = self.c[(i + 1):(self.d + 1)]
        self.s[i:(self.d - 1)] = self.s[(i + 1):self.d]
        self.d = len(self.c) - 1

    def removeRec(self, key, h):
        i = self.locateLocally(key)
        if h == 1:
            if self.c[i].key == key:
                self.c[i].remove()
                self.removeLocally(i)
        else:
            self.c[i].removeRec(key, (h - 1))
            if self.c[i].d < A:
                if i == self.d:
                    i -= 1

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

                    d1 = len(c1) - 1

                    if d1 <= B:
                        self.c[i + 1].s = s1
                        self.c[i + 1].c = c1
                        self.c[i + 1].d = d1

                    else:
                        m = ceil(d1 / 2)

                        self.c[i].s = s1[0:m]
                        self.c[i].c = c1[0:(m + 1)]
                        self.c[i].d = m

                        self.c[i + 1].s = s1[(m + 1):d1]
                        self.c[i + 1].c = c1[(m + 1):(d1 + 1)]
                        self.c[i + 1].d = d1 - m

                        self.s[i] = s1[m]

    def mergeRec(self, lvl, root, splitter, l_r):
        i = self.locateLocally(l_r)
        if lvl == 0:
            root.s[-1] = splitter
            k, t = root.s[1:], root.c[1:]

        else:
            k, t = self.c[i].mergeRec((lvl - 1), root, splitter, l_r)
            if t is None:
                return None, None

        s1 = [float('-inf')]
        for x in range(1, i, 1):
            s1.append(self.s[x])
        if isinstance(k, list):
            for element in k:
                s1.append(element)
        else:
            s1.append(k)
        for x in range(i, self.d + 1, 1):
            s1.append(self.s[x])

        c1 = [None]
        for x in range(1, i, 1):
            c1.append(self.c[x])
        if isinstance(t, list):
            for child in t:
                c1.append(child)
        else:
            c1.append(t)
        for x in range(i, self.d + 1, 1):
            c1.append(self.c[x])

        d1 = len(c1) - 1

        if d1 <= B:
            self.s, self.c, self.d = s1, c1, d1
            return None, None
        else:
            self.d = floor(d1 / 2)

            self.s = s1[(-self.d):]
            self.s.insert(0, float('-inf'))

            self.c = c1[(-self.d):]
            self.c.insert(0, None)

            return s1[B + 1 - self.d], Node(
                c1[1:(-self.d)], s1[1:(-self.d - 1)])


class ABTree:
    """An (a,b)-Tree, represented as a root.
    Also contains a list/its head and the height"""

    def __init__(self):
        self.list = DoublyLinkedList()
        self.root = Node([self.list.head])
        self.height = 1

    def locate(self, key):
        return self.root.locateRec(key, self.height)

    def insert(self, key, value):
        k, t = self.root.insertRec(key, value, self.height)
        if t is not None:
            self.root = Node([t, self.root], k)
            self.height += 1

    def remove(self, key):
        self.root.removeRec(key, self.height)
        if self.root == 1 and self.height > 1:
            old = self.root
            self.root = old.c[1]
            del old
            self.height -= 1

    def listAll(self):
        self.list.listAll()

    def count(self):
        return self.list.count()

    def first(self):
        return self.list.first()

    def last(self):
        return self.list.last()

    def locateRange(self, start, end):
        current = self.locate(start)
        result = []
        while current.key <= end:
            result.append(current)
            current = current.succ
        return result


# =================================================
# MERGE ===========================================
# =================================================

def mergeTrees(tree_1, tree_2):
    if tree_1.last().key >= tree_2.first().key:
        if tree_2.last().key >= tree_1.first().key:
            return None
        else:
            tree_1, tree_2 = tree_2, tree_1

    tree_1.last().succ = tree_2.first()
    tree_2.first().prev = tree_1.last()

    tree_1.first().prev = tree_2.list.head
    tree_2.list.head.succ = tree_1.first()

    if tree_1.height >= tree_2.height:
        tree_1.list = tree_2.list
        k, t = tree_1.root.mergeRec((tree_1.height - tree_2.height),
                                    tree_2.root,
                                    tree_1.last().key,
                                    float('inf'))
        if t is not None:
            tree_1.root = Node([t, tree_1.root], k)
            tree_1.height += 1
        return tree_1

    else:
        k, t = tree_2.root.mergeRec((tree_2.height - tree_1.height),
                                    tree_1.root,
                                    tree_1.last().key,
                                    float('-inf'))
        if t is not None:
            tree_2.root = Node([t, tree_2.root], k)
            tree_2.height += 1
        return tree_2
