from dll import *

class Node:

    def splitRec(self, key, height, head, first):
        i = self.locateLocally(key)
        if height == 1:
            self.c[i].prev.succ = Leaf(float('inf'), self.c[i].prev, first)
            first.prev = self.c[i].prev.succ

            self.c[i].prev = head
            head.succ = self.c[i]
            # two linked lists

    def getHeightRec(self):
        if isinstance(self.c[1], Leaf):
            return 1
        else:
            return 1 + self.c[1].getHeightRec()


class ABTree:
    def split(self, key):
        tree_1, tree_2 = ABTree(), ABTree()
        tree_1.root, tree_2.root = self.root.splitRec(
            key, self.height, self.list.head, self.first())
        tree_1.list.height = tree_1.getHeight()
        tree_2.list.height = tree_2.getHeight()
        tree_1.list.head = tree_1.getHead()
        tree_2.list.head = tree_2.getHead()
        return tree_1, tree_2

    def getHeight(self):
        return self.root.getHeightRec()

    def getHead(self):
        return self.root.locateRec(float('inf'), self.height)
