from time import sleep

class Leaf:
    """An element of a doubly linked list"""

    def __init__(self, key, prev=None, succ=None, value=None):
        self.key = key
        self.prev = prev
        self.succ = succ
        self.value = value

    def insertAfter(self, key, value=None):
        new = Leaf(key, self, self.succ, value)
        self.succ.prev = new
        self.succ = new
        return new

    def insertBefore(self, key, value=None):
        return self.prev.insertAfter(key, value)

    def remove(self):
        self.prev.succ = self.succ
        self.succ.prev = self.prev
        del self


class DoublyLinkedList:
    """A Doubly Linked List, represented as the Head/dummy element"""

    def __init__(self):
        self.head = Leaf(float('inf'))
        self.head.prev = self.head
        self.head.succ = self.head

    def locate(self, key):
        current = self.head.succ
        while current.key <= key:
            current = current.succ
        return current.prev

    def insert(self, key, value=None):
        target = self.locate(key)
        if target.key == key:
            target.value = value
        else:
            new = Leaf(key, target, target.succ, value)
            target.succ.prev = new
            target.succ = new

    def remove(self, key):
        target = self.locate(key)
        if target.key == key:
            target.prev.succ = target.succ
            target.succ.prev = target.prev
            del target

    def isEmpty(self):
        if self.head.succ == self.head:
            return True
        return False

    def listAll(self):
        current = self.head.succ
        while current != self.head:
            print(f'{current.key}: {current.value}')
            current = current.succ
            sleep(0.001)

    def count(self):
        current = self.head.succ
        i = 0
        while current != self.head:
            i += 1
            current = current.succ
        return i

    def first(self):
        if self.isEmpty():
            return None
        return self.head.succ

    def last(self):
        if self.isEmpty():
            return None
        return self.head.prev
