"""装饰器模式 - 高级示例"""
from abc import ABC, abstractmethod
from typing import List
from enum import Enum


class Size(Enum):
    SMALL = ("小杯", 8)
    MEDIUM = ("中杯", 12)
    LARGE = ("大杯", 15)


class Sugar(Enum):
    NONE = "无糖"
    LESS = "少糖"
    NORMAL = "正常糖"
    EXTRA = "多糖"


class Bean(Enum):
    ROBUSTA = ("罗布斯塔", 0)
    ARABICA = ("阿拉比卡", 5)
    BLEND = ("混合", 2)


class Coffee(ABC):
    @abstractmethod
    def get_cost(self) -> int: pass
    @abstractmethod
    def get_desc(self) -> str: pass
    @abstractmethod
    def get_ings(self) -> List[str]: pass


class SimpleCoffee(Coffee):
    def __init__(self, size=Size.MEDIUM, bean=Bean.BLEND):
        self._size = size
        self._bean = bean
        self._sugar = Sugar.NORMAL

    def get_cost(self) -> int:
        return self._size.value[1] + self._bean.value[1]

    def get_desc(self) -> str:
        return f"{self._size.value[0]}{self._bean.value[0]}咖啡({self._sugar.value})"

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


class SugarD(CoffeeDecorator):
    def __init__(self, c, level):
        super().__init__(c)
        self._level = level

    def get_cost(self) -> int:
        return self._c.get_cost() + 2

    def get_desc(self) -> str:
        return self._c.get_desc()

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
        return self._c.get_cost() + 3

    def get_desc(self) -> str:
        return "冰" + self._c.get_desc()

    def get_ings(self) -> List[str]:
        return self._c.get_ings() + ["冰"]


def show(c):
    print(f"商品: {c.get_desc()}")
    print(f"配料: {', '.join(c.get_ings())}")
    print(f"总价: {c.get_cost()}元")


if __name__ == "__main__":
    print("=== 咖啡店菜单 ===\n")
    print("1. 基础咖啡:")
    show(SimpleCoffee(Size.MEDIUM, Bean.BLEND))
    print("\n2. 阿拉比卡(少糖):")
    show(SugarD(SimpleCoffee(Size.MEDIUM, Bean.ARABICA), Sugar.LESS))
    print("\n3. 冰焦糖玛奇朵:")
    show(Ice(Caramel(Milk(SimpleCoffee(Size.LARGE, Bean.ARABICA)))))
    print("\n4. 豪华摩卡:")
    show(Ice(Caramel(WhippedCream(Milk(SimpleCoffee(Size.LARGE, Bean.ARABICA))))))
