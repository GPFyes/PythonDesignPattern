"""装饰器模式 - 简单级示例"""
from abc import ABC, abstractmethod


class Coffee(ABC):
    @abstractmethod
    def get_cost(self) -> int: pass
    @abstractmethod
    def get_desc(self) -> str: pass


class SimpleCoffee(Coffee):
    def get_cost(self) -> int:
        return 10
    def get_desc(self) -> str:
        return "基础咖啡"


class CoffeeDecorator(Coffee):
    def __init__(self, c):
        self._c = c
    def get_cost(self) -> int:
        return self._c.get_cost()
    def get_desc(self) -> str:
        return self._c.get_desc()


class Milk(CoffeeDecorator):
    def get_cost(self) -> int:
        return self._c.get_cost() + 5
    def get_desc(self) -> str:
        return self._c.get_desc() + "+牛奶"


class Sugar(CoffeeDecorator):
    def get_cost(self) -> int:
        return self._c.get_cost() + 2
    def get_desc(self) -> str:
        return self._c.get_desc() + "+糖"


class WhippedCream(CoffeeDecorator):
    def get_cost(self) -> int:
        return self._c.get_cost() + 8
    def get_desc(self) -> str:
        return self._c.get_desc() + "+奶油"


class Caramel(CoffeeDecorator):
    def get_cost(self) -> int:
        return self._c.get_cost() + 6
    def get_desc(self) -> str:
        return self._c.get_desc() + "+焦糖"


if __name__ == "__main__":
    c = SimpleCoffee()
    print(f"简单咖啡: {c.get_cost()}元")
    print(f"加牛奶: {Milk(c).get_desc()}, {Milk(c).get_cost()}元")
    print(f"加牛奶糖: {Sugar(Milk(c)).get_desc()}, {Sugar(Milk(c)).get_cost()}元")
    print(f"豪华: {Caramel(WhippedCream(Milk(c))).get_desc()}")
    print(f"总价: {Caramel(WhippedCream(Milk(c))).get_cost()}元")
