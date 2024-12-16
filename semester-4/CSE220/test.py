class Node:
    def __init__(self, value=None, next=None):
        self.value = value
        self.next = next


class HashTable:
    def __init__(self, length):
        self.ht = [None] * length
        self.length = length

    def show(self):
        count = 0
        for i in self.ht:
            temp = i
            print(count, end=" ")
            while temp is not None:
                print(temp.value, end="-->")
                temp = temp.next
            count += 1
            print()

    def __hash_function(self, key):
        sum_ascii = 0
        if len(key) % 2 == 0:
            for i in range(0, len(key), 2):
                sum_ascii += ord(key[i])
        else:
            for i in range(1, len(key), 2):
                sum_ascii += ord(key[i])
        return sum_ascii % self.length

    def insert(self, key, value):
        index = self.__hash_function(key)
        new_node = Node((key, value))

        if self.ht[index] is None:
            self.ht[index] = new_node
        else:
            current = self.ht[index]
            prev = None
            while current is not None and current.value[1] > value:
                prev = current
                current = current.next
            if prev is None:
                new_node.next = self.ht[index]
                self.ht[index] = new_node
            else:
                new_node.next = current
                prev.next = new_node


# Driver Code
ht = HashTable(3)

print("------Test#1------")
ht.insert("apple", 20)
ht.insert("coconut", 90)
ht.insert("cherry", 50)
ht.show()

print("------Test#2------")
ht.insert("banana", 30)
ht.insert("pineapple", 50)
ht.show()

print("------Test#3------")
ht.insert("apple", 100)
ht.insert("Guava", 10)
ht.show()
