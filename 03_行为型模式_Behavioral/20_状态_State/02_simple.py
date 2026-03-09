"""
State Pattern - Simple Level
自动售货机简单示例：带商品库存和找零功能
"""

from abc import ABC, abstractmethod
from enum import Enum


class Product(Enum):
    COLA = ("可乐", 3)
    CHIPS = ("薯片", 5)
    WATER = ("矿泉水", 2)

    def __init__(self, name, price):
        self.name = name
        self.price = price


class State(ABC):
    @abstractmethod
    def insert_money(self, machine, amount):
        pass

    @abstractmethod
    def select_product(self, machine, product):
        pass

    @abstractmethod
    def return_money(self, machine):
        pass


class NoMoneyState(State):
    def insert_money(self, machine, amount):
        machine.add_money(amount)
        print(f"投币：{amount}元")
        if machine.total_money > 0:
            machine.set_state(machine.has_money_state)

    def select_product(self, machine, product):
        print("请先投币！")

    def return_money(self, machine):
        print("没有投币，无法找零！")


class HasMoneyState(State):
    def insert_money(self, machine, amount):
        machine.add_money(amount)
        print(f"继续投币：{amount}元，总计：{machine.total_money}元")

    def select_product(self, machine, product):
        if product.value.price <= machine.total_money:
            if machine.get_stock(product) > 0:
                machine.deduct_stock(product)
                change = machine.total_money - product.value.price
                machine.set_money(0)
                print(f"出货：{product.value.name}，找零：{change}元")
                machine.set_state(machine.no_money_state)
            else:
                print(f"{product.value.name} 已售罄！")
        else:
            print(f"金额不足！{product.value.name} 需要{product.value.price}元，当前{machine.total_money}元")

    def return_money(self, machine):
        print(f"找零：{machine.total_money}元")
        machine.set_money(0)
        machine.set_state(machine.no_money_state)


class VendingMachine:
    def __init__(self):
        self.no_money_state = NoMoneyState()
        self.has_money_state = HasMoneyState()
        self.current_state = self.no_money_state
        self.total_money = 0
        self.stock = {Product.COLA: 5, Product.CHIPS: 3, Product.WATER: 10}

    def set_state(self, state):
        self.current_state = state

    def add_money(self, amount):
        self.total_money += amount

    def set_money(self, amount):
        self.total_money = amount

    def get_stock(self, product):
        return self.stock.get(product, 0)

    def deduct_stock(self, product):
        if product in self.stock:
            self.stock[product] -= 1

    def insert_money(self, amount):
        self.current_state.insert_money(self, amount)

    def select_product(self, product):
        self.current_state.select_product(self, product)

    def return_money(self):
        self.current_state.return_money(self)

    def show_stock(self):
        print("\n=== 商品库存 ===")
        for product, count in self.stock.items():
            print(f"{product.value.name}: {count}件，{product.value.price}元")


if __name__ == "__main__":
    machine = VendingMachine()
    machine.show_stock()

    print("\n=== 场景1：投币不足 ===")
    machine.insert_money(1)
    machine.select_product(Product.COLA)

    print("\n=== 场景2：投币足够，购买成功 ===")
    machine.insert_money(2)
    machine.select_product(Product.COLA)

    print("\n=== 场景3：投币后找零 ===")
    machine.insert_money(10)
    machine.select_product(Product.CHIPS)

    print("\n=== 场景4：购买已售罄商品 ===")
    for _ in range(6):
        machine.insert_money(5)
        machine.select_product(Product.COLA)

    print("\n=== 最终库存 ===")
    machine.show_stock()
