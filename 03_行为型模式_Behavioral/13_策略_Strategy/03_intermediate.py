from abc import ABC, abstractmethod
from typing import Dict, List


class DiscountStrategy(ABC):
    @abstractmethod
    def calculate(self, price: float) -> float:
        pass


class NoDiscount(DiscountStrategy):
    def calculate(self, price: float) -> float:
        return price


class PercentageDiscount(DiscountStrategy):
    def __init__(self, percentage: float):
        self.percentage = percentage

    def calculate(self, price: float) -> float:
        return price * (1 - self.percentage / 100)


class FixedDiscount(DiscountStrategy):
    def __init__(self, amount: float):
        self.amount = amount

    def calculate(self, price: float) -> float:
        return max(price - self.amount, 0)


class VIPDiscount(DiscountStrategy):
    def __init__(self, vip_level: int):
        self.vip_level = vip_level

    def calculate(self, price: float) -> float:
        discount_rate = min(self.vip_level * 0.05, 0.5)
        return price * (1 - discount_rate)


class Product:
    def __init__(self, name: str, price: float):
        self.name = name
        self.price = price


class ShoppingCart:
    def __init__(self):
        self.items: List[Product] = []
        self.discount_strategy: DiscountStrategy = NoDiscount()

    def add_item(self, product: Product):
        self.items.append(product)

    def set_discount(self, strategy: DiscountStrategy):
        self.discount_strategy = strategy

    def get_subtotal(self) -> float:
        return sum(item.price for item in self.items)

    def get_total(self) -> float:
        subtotal = self.get_subtotal()
        return self.discount_strategy.calculate(subtotal)

    def show_details(self):
        print("购物车商品:")
        for item in self.items:
            print(f"  - {item.name}: ¥{item.price}")
        print(f"小计: ¥{self.get_subtotal()}")
        print(f"折扣后: ¥{self.get_total()}")


if __name__ == "__main__":
    cart = ShoppingCart()
    cart.add_item(Product("iPhone 15", 6999))
    cart.add_item(Product("AirPods Pro", 1999))

    print("=== 无折扣 ===")
    cart.show_details()

    print("\n=== 10%折扣 ===")
    cart.set_discount(PercentageDiscount(10))
    cart.show_details()

    print("\n=== 满500减100 ===")
    cart.set_discount(FixedDiscount(100))
    cart.show_details()

    print("\n=== VIP3会员 ===")
    cart.set_discount(VIPDiscount(3))
    cart.show_details()
