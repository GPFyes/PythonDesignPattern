"""装饰器模式 - 中级示例"""
from abc import ABC, abstractmethod
from typing import List


class Coffee(ABC):
    @abstractmethod
    def get_cost(self) -> int: pass
    @abstractmethod
    def get_desc(self) -> str: pass
    @abstractmethod
    def get_ings(self) -> List[str]: pass


class SimpleCoffee(Coffee):
    def __init__(self, size="中杯"):
        self._size = size
        self._p = {"小杯": 8, "中杯": 10, "大杯": 12}
    def get_cost(self) -> int:
        return self._p.get(self._size, 10)
    def get_desc(self) -> str:
        return f"{self._size}咖啡"
    def get_ings(self) -> List[str]:
        return ["咖啡"]


class CoffeeDecorator(Coffee):
    def __init__(self, c):
        self._c = c
    def get_cost(self) -> int:
        return self._c.get_cost()
    def get_desc(self) -> str:
        return self._c.get_desc()
    def get_ings(self) -> List[str]:
        return self._c.get_ings()


class Milk(CoffeeDecorator):
    def get_cost(self) -> int:
        return self._c.get_cost() + 5
    def get_desc(self) -> str:
        return self._c.get_desc() + "+牛奶"
    def get_ings(self) -> List[str]:
        return self._c.get_ings() + ["牛奶"]


class Sugar(CoffeeDecorator):
    def get_cost(self) -> int:
        return self._c.get_cost() + 2
    def get_desc(self) -> str:
        return self._c.get_desc() + "+糖"
    def get_ings(self) -> List[str]:
        return self._c.get_ings() + ["糖"]


class WhippedCream(CoffeeDecorator):
    def get_cost(self) -> int:
        return self._c.get_cost() + 8
    def get_desc(self) -> str:
        return self._c.get_desc() + "+奶油"
    def get_ings(self) -> List[str]:
        return self._c.get_ings() + ["奶油"]


class Caramel(CoffeeDecorator):
    def get_cost(self) -> int:
        return self._c.get_cost() + 6
    def get_desc(self) -> str:
        return self._c.get_desc() + "+焦糖"
    def get_ings(self) -> List[str]:
        return self._c.get_ings() + ["焦糖"]


class Ice(CoffeeDecorator):
    def get_cost(self) -> int:
        return self._c.get_cost() + 2
    def get_desc(self) -> str:
        return "冰" + self._c.get_desc()
    def get_ings(self) -> List[str]:
        return self._c.get_ings() + ["冰"]


def show(c):
    print(f"描述: {c.get_desc()}")
    print(f"价格: {c.get_cost()}元")
    print(f"配料: {', '.join(c.get_ings())}")


if __name__ == "__main__":
    print("=== 大杯咖啡 ===")
    show(SimpleCoffee("大杯"))
    print("\n=== 冰焦糖玛奇朵 ===")
    show(Ice(Caramel(Milk(SimpleCoffee("中杯")))))
    print("\n=== 豪华咖啡 ===")
    show(Ice(Caramel(WhippedCream(Milk(SimpleCoffee("大杯"))))))
