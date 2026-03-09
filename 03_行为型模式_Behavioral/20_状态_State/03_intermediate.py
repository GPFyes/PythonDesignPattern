"""
State Pattern - Intermediate Level
自动售货机中级示例：支持多种支付方式和促销
"""

from abc import ABC, abstractmethod
from enum import Enum
from datetime import datetime


class Product(Enum):
    COLA = ("可乐", 3, 10)
    CHIPS = ("薯片", 5, 8)
    WATER = ("矿泉水", 2, 15)
    CANDY = ("糖果", 1, 20)

    def __init__(self, name, price, stock):
        self.name = name
        self.price = price
        self.stock = stock


class PaymentMethod(Enum):
    CASH = "现金"
    WECHAT = "微信"
    ALIPAY = "支付宝"


class State(ABC):
    @abstractmethod
    def insert_money(self, machine, amount, method):
        pass

    @abstractmethod
    def select_product(self, machine, product):
        pass

    @abstractmethod
    def cancel(self, machine):
        pass


class NoMoneyState(State):
    def insert_money(self, machine, amount, method=PaymentMethod.CASH):
        if amount > 0:
            machine.add_money(amount)
            machine.set_payment_method(method)
            print(f"投币：{amount}元，支付方式：{method.value}")
            machine.set_state(machine.has_money_state)
        else:
            print("投币金额必须大于0！")

    def select_product(self, machine, product):
        print("请先投币！")

    def cancel(self, machine):
        print("没有投币，无法取消！")


class HasMoneyState(State):
    def insert_money(self, machine, amount, method=PaymentMethod.CASH):
        if amount > 0:
            machine.add_money(amount)
            machine.set_payment_method(method)
            print(f"继续投币：{amount}元，总计：{machine.total_money}元")
        else:
            print("投币金额必须大于0！")

    def select_product(self, machine, product):
        price = machine.get_discounted_price(product)
        
        if machine.get_stock(product) <= 0:
            print(f"{product.value.name} 已售罄！")
            return
        
        if machine.total_money >= price:
            machine.deduct_stock(product)
            change = machine.total_money - price
            machine.add_sales(price)
            
            print(f"出货：{product.value.name}，原价：{product.value.price}元，优惠价：{price}元")
            if change > 0:
                print(f"找零：{change}元")
            
            machine.set_money(0)
            machine.set_payment_method(None)
            machine.set_state(machine.no_money_state)
        else:
            print(f"金额不足！{product.value.name} 需要{price}元，当前{machine.total_money}元")

    def cancel(self, machine):
        print(f"交易取消，找零：{machine.total_money}元")
        machine.set_money(0)
        machine.set_payment_method(None)
        machine.set_state(machine.no_money_state)


class VendingMachine:
    def __init__(self):
        self.no_money_state = NoMoneyState()
        self.has_money_state = HasMoneyState()
        self.current_state = self.no_money_state
        
        self.total_money = 0
        self.payment_method = None
        self.stock = {p: p.value.stock for p in Product}
        self.sales = 0
        self.promotion_active = False
        self.promotion_discount = 0.8

    def set_state(self, state):
        self.current_state = state

    def add_money(self, amount):
        self.total_money += amount

    def set_money(self, amount):
        self.total_money = amount

    def set_payment_method(self, method):
        self.payment_method = method

    def get_stock(self, product):
        return self.stock.get(product, 0)

    def deduct_stock(self, product):
        if product in self.stock:
            self.stock[product] -= 1

    def get_discounted_price(self, product):
        base_price = product.value.price
        if self.promotion_active:
            return int(base_price * self.promotion_discount)
        if self.payment_method in [PaymentMethod.WECHAT, PaymentMethod.ALIPAY]:
            return int(base_price * 0.95)
        return base_price

    def add_sales(self, amount):
        self.sales += amount

    def activate_promotion(self, discount=0.8):
        self.promotion_active = True
        self.promotion_discount = discount
        print(f"促销活动开启！全场{discount*10}折")

    def deactivate_promotion(self):
        self.promotion_active = False
        print("促销活动结束")

    def insert_money(self, amount, method=PaymentMethod.CASH):
        self.current_state.insert_money(self, amount, method)

    def select_product(self, product):
        self.current_state.select_product(self, product)

    def cancel(self):
        self.current_state.cancel(self)

    def show_info(self):
        print(f"\n=== 售货机状态 ===")
        print(f"当前金额：{self.total_money}元")
        print(f"支付方式：{self.payment_method.value if self.payment_method else '无'}")
        print(f"总销售额：{self.sales}元")
        print(f"促销状态：{'开启' if self.promotion_active else '关闭'}")
        
        print("\n=== 商品库存 ===")
        for product in Product:
            stock = self.get_stock(product)
            price = self.get_discounted_price(product)
            original = product.value.price
            discount_info = f" (原价:{original}元)" if price != original else ""
            print(f"{product.value.name}: {stock}件，{price}元{discount_info}")


if __name__ == "__main__":
    machine = VendingMachine()
    machine.show_info()

    print("\n=== 场景1：现金购买 ===")
    machine.insert_money(5)
    machine.select_product(Product.COLA)

    print("\n=== 场景2：微信支付购买 ===")
    machine.insert_money(10, PaymentMethod.WECHAT)
    machine.select_product(Product.CHIPS)

    print("\n=== 场景3：余额不足 ===")
    machine.insert_money(1)
    machine.select_product(Product.COLA)

    print("\n=== 场景4：取消交易 ===")
    machine.insert_money(10)
    machine.cancel()

    print("\n=== 场景5：促销活动 ===")
    machine.activate_promotion(0.8)
    machine.insert_money(5)
    machine.select_product(Product.CANDY)
    machine.deactivate_promotion()

    print("\n=== 场景6：购买售罄商品 ===")
    for _ in range(15):
        machine.insert_money(5)
        machine.select_product(Product.CANDY)

    machine.show_info()
