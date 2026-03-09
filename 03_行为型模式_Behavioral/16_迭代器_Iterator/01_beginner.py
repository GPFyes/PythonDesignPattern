from abc import ABC, abstractmethod
from typing import Any, List


class Iterator(ABC):
    @abstractmethod
    def has_next(self) -> bool:
        pass

    @abstractmethod
    def next(self) -> Any:
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


class ArrayCollection:
    def __init__(self):
        self._items: List[Any] = []

    def add(self, item: Any):
        self._items.append(item)

    def create_iterator(self) -> Iterator:
        return ArrayIterator(self._items)


if __name__ == "__main__":
    collection = ArrayCollection()
    collection.add("苹果")
    collection.add("香蕉")
    collection.add("橙子")

    iterator = collection.create_iterator()
    while iterator.has_next():
        print(iterator.next())
