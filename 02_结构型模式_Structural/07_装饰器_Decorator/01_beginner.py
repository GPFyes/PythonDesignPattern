"""装饰器模式 - 入门级示例"""
from abc import ABC, abstractmethod


class Coffee(ABC):
    @abstractmethod
    def get_cost(self) -> int: pass


class SimpleCoffee(Coffee):
    def get_cost(self) -> int:
        return 10


class CoffeeDecorator(Coffee):
    def __init__(self, coffee):
        self._coffee = coffee
    def get_cost(self) -> int:
        return self._coffee.get_cost()


class Milk(CoffeeDecorator):
    def get_cost(self) -> int:
        return self._coffee.get_cost() + 3


class Sugar(CoffeeDecorator):
    def get_cost(self) -> int:
        return self._coffee.get_cost() + 2


if __name__ == "__main__":
    print(f"咖啡: {SimpleCoffee().get_cost()}元")
    print(f"咖啡+牛奶: {Milk(SimpleCoffee()).get_cost()}元")
    print(f"咖啡+牛奶+糖: {Sugar(Milk(SimpleCoffee())).get_cost()}元")
