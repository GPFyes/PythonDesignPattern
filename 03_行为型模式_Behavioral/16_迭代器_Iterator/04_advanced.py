from abc import ABC, abstractmethod
from typing import Any, List, Callable, Optional, Iterator as TypingIterator


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


class FilteredIterator(Iterator):
    def __init__(self, data: List[Any], predicate: Optional[Callable[[Any], bool]] = None):
        self._original_data = data
        self._filtered_data = [item for item in data if predicate is None or predicate(item)]
        self._position = 0

    def has_next(self) -> bool:
        return self._position < len(self._filtered_data)

    def next(self) -> Any:
        if self.has_next():
            item = self._filtered_data[self._position]
            self._position += 1
            return item
        return None

    def reset(self):
        self._position = 0


class TransformedIterator(Iterator):
    def __init__(self, data: List[Any], transform: Callable[[Any], Any]):
        self._data = data
        self._transform = transform
        self._position = 0

    def has_next(self) -> bool:
        return self._position < len(self._data)

    def next(self) -> Any:
        if self.has_next():
            item = self._data[self._position]
            self._position += 1
            return self._transform(item)
        return None

    def reset(self):
        self._position = 0


class ChainIterator(Iterator):
    def __init__(self, iterators: List[Iterator]):
        self._iterators = iterators
        self._current_index = 0
        self._current_iterator = iterators[0] if iterators else None

    def has_next(self) -> bool:
        while self._current_iterator and not self._current_iterator.has_next():
            self._current_index += 1
            if self._current_index < len(self._iterators):
                self._current_iterator = self._iterators[self._current_index]
            else:
                self._current_iterator = None
                return False
        return True

    def next(self) -> Any:
        if self.has_next() and self._current_iterator:
            return self._current_iterator.next()
        return None

    def reset(self):
        self._current_index = 0
        self._current_iterator = self._iterators[0] if self._iterators else None
        for it in self._iterators:
            it.reset()


class Collection(ABC):
    @abstractmethod
    def create_iterator(self) -> Iterator:
        pass

    @abstractmethod
    def add(self, item: Any):
        pass


class ProductCollection(Collection):
    def __init__(self):
        self._products: List[dict] = []

    def add(self, item: dict):
        self._products.append(item)

    def create_iterator(self) -> Iterator:
        return FilteredIterator(self._products)

    def create_filtered_iterator(self, predicate: Callable[[dict], bool]) -> Iterator:
        return FilteredIterator(self._products, predicate)

    def create_transformed_iterator(self, transform: Callable[[dict], Any]) -> Iterator:
        return TransformedIterator(self._products, transform)

    def get_all(self) -> List[dict]:
        return self._products


def filter_expensive(products: List[dict], min_price: float) -> List[dict]:
    return [p for p in products if p.get("price", 0) >= min_price]


def transform_to_names(products: List[dict]) -> List[str]:
    return [p.get("name", "") for p in products]


if __name__ == "__main__":
    products = ProductCollection()
    products.add({"name": "手机", "price": 5000})
    products.add({"name": "电脑", "price": 8000})
    products.add({"name": "平板", "price": 3000})
    products.add({"name": "耳机", "price": 500})
    products.add({"name": "手表", "price": 2000})

    print("=== 所有产品 ===")
    all_iter = products.create_iterator()
    while all_iter.has_next():
        p = all_iter.next()
        print(f"{p['name']}: ¥{p['price']}")

    print("\n=== 价格 >= 2000 的产品 ===")
    expensive_iter = products.create_filtered_iterator(lambda p: p["price"] >= 2000)
    while expensive_iter.has_next():
        p = expensive_iter.next()
        print(f"{p['name']}: ¥{p['price']}")

    print("\n=== 产品名称列表 ===")
    name_iter = products.create_transformed_iterator(lambda p: p["name"])
    while name_iter.has_next():
        print(name_iter.next())

    print("\n=== 链式迭代 ===")
    chain = ChainIterator([
        FilteredIterator(products.get_all(), lambda p: p["price"] < 2000),
        FilteredIterator(products.get_all(), lambda p: p["price"] >= 2000)
    ])
    while chain.has_next():
        p = chain.next()
        print(f"{p['name']}: ¥{p['price']}")
