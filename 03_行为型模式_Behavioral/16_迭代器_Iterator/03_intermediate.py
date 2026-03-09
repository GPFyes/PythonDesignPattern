from abc import ABC, abstractmethod
from typing import Any, List


class Iterator(ABC):
    @abstractmethod
    def has_next(self) -> bool:
        pass

    @abstractmethod
    def next(self) -> Any:
        pass

    @abstractmethod
    def reset(self):
        pass


class ArrayIterator(Iterator):
    def __init__(self, data: List[Any]):
        self._data = data
        self._position = 0

    def has_next(self) -> bool:
        return self._position < len(self._data)

    def next(self) -> Any:
        if self.has_next():
            item = self._data[self._position]
            self._position += 1
            return item
        return None

    def reset(self):
        self._position = 0


class LinkedListIterator(Iterator):
    class Node:
        def __init__(self, data: Any):
            self.data = data
            self.next = None

    def __init__(self, head: Node):
        self._head = head
        self._current = head

    def has_next(self) -> bool:
        return self._current is not None

    def next(self) -> Any:
        if self.has_next():
            item = self._current.data
            self._current = self._current.next
            return item
        return None

    def reset(self):
        self._current = self._head


class Collection(ABC):
    @abstractmethod
    def create_iterator(self) -> Iterator:
        pass

    @abstractmethod
    def count(self) -> int:
        pass


class ArrayCollection(Collection):
    def __init__(self):
        self._items: List[Any] = []

    def add(self, item: Any):
        self._items.append(item)

    def create_iterator(self) -> Iterator:
        return ArrayIterator(self._items)

    def count(self) -> int:
        return len(self._items)


class LinkedList(Collection):
    class _Node:
        def __init__(self, data: Any):
            self.data = data
            self.next = None

    def __init__(self):
        self._head = None
        self._tail = None
        self._size = 0

    def add(self, item: Any):
        new_node = self._Node(item)
        if self._head is None:
            self._head = new_node
            self._tail = new_node
        else:
            self._tail.next = new_node
            self._tail = new_node
        self._size += 1

    def create_iterator(self) -> Iterator:
        return LinkedListIterator(self._head)

    def count(self) -> int:
        return self._size


def traverse_collection(collection: Collection):
    iterator = collection.create_iterator()
    print(f"集合元素数量: {collection.count()}")
    while iterator.has_next():
        print(iterator.next())


if __name__ == "__main__":
    print("=== 数组集合遍历 ===")
    arr = ArrayCollection()
    arr.add("A")
    arr.add("B")
    arr.add("C")
    traverse_collection(arr)

    print("\n=== 链表集合遍历 ===")
    linked = LinkedList()
    linked.add(10)
    linked.add(20)
    linked.add(30)
    traverse_collection(linked)
