from abc import ABC, abstractmethod
from typing import Any, List


class Iterator(ABC):
    @abstractmethod
    def has_next(self) -> bool:
        pass

    @abstractmethod
    def next(self) -> Any:
        pass


class ForwardIterator(Iterator):
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


class ReverseIterator(Iterator):
    def __init__(self, data: List[Any]):
        self._data = data
        self._position = len(data) - 1

    def has_next(self) -> bool:
        return self._position >= 0

    def next(self) -> Any:
        if self.has_next():
            item = self._data[self._position]
            self._position -= 1
            return item
        return None


class NumberCollection:
    def __init__(self):
        self._numbers: List[int] = []

    def add(self, num: int):
        self._numbers.append(num)

    def create_forward_iterator(self) -> Iterator:
        return ForwardIterator(self._numbers)

    def create_reverse_iterator(self) -> Iterator:
        return ReverseIterator(self._numbers)


if __name__ == "__main__":
    numbers = NumberCollection()
    for i in [1, 2, 3, 4, 5]:
        numbers.add(i)

    print("正向遍历:")
    f_iter = numbers.create_forward_iterator()
    while f_iter.has_next():
        print(f_iter.next(), end=" ")
    print()

    print("反向遍历:")
    r_iter = numbers.create_reverse_iterator()
    while r_iter.has_next():
        print(r_iter.next(), end=" ")
    print()
