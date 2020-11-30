
class Leaf:
    """An element of a doubly linked list"""

    def __init__(self, key, prev=None, succ=None, value=None):
        self.key = key
        self.prev = prev
        self.succ = succ
        self.value = value

    def insertAfter(self, key, value=None):
        '''inserts a new leaf after this leaf'''

        new = Leaf(key, self, self.succ, value)
        self.succ.prev = new
        self.succ = new
        return new

    def insertBefore(self, key, value=None):
        '''inserts a new leaf before this leaf'''
        return self.prev.insertAfter(key, value)

    def remove(self):
        '''removes this leave'''
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
        '''locates an element in the list
        by iterating through it'''
        current = self.head.succ
        while current.key <= key:
            current = current.succ
        return current.prev

    def insert(self, key, value=None):
        '''inserts an element in the list'''

        target = self.locate(key)
        if target.key == key:
            target.value = value
        else:
            new = Leaf(key, target, target.succ, value)
            target.succ.prev = new
            target.succ = new

    def remove(self, key):
        '''removes an element from the list'''

        target = self.locate(key)
        if target.key == key:
            target.prev.succ = target.succ
            target.succ.prev = target.prev
            del target

    def isEmpty(self):
        '''checks if list is empty'''

        if self.head.succ == self.head:
            return True
        return False

    def listAll(self):
        '''lists all elements of the list on the command line'''
        current = self.head.succ
        while current != self.head:
            print(f'{current.key}: {current.value}')
            current = current.succ

    def count(self):
        '''counts how many elements list is containing'''

        current = self.head.succ
        i = 0
        while current != self.head:
            i += 1
            current = current.succ
        return i

    def first(self):
        '''returns first element in list'''
        if self.isEmpty():
            return None
        return self.head.succ

    def last(self):
        '''returns last element in list'''
        if self.isEmpty():
            return None
        return self.head.prev
