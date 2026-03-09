from abc import ABC, abstractmethod
from typing import Optional


class PayStrategy(ABC):
    @abstractmethod
    def pay(self, amount: float) -> str:
        pass


class CreditCard(PayStrategy):
    def __init__(self, card: str):
        self.card = card

    def pay(self, amount: float) -> str:
        return f"信用卡{self.card[-4:]}付{amount}元"


class PayPal(PayStrategy):
    def __init__(self, email: str):
        self.email = email

    def pay(self, amount: float) -> str:
        return f"PayPal{self.email}付{amount}元"


class Cart:
    def __init__(self):
        self.items = []
        self.strategy: Optional[PayStrategy] = None

    def add(self, name: str, price: float):
        self.items.append(price)

    def checkout(self) -> str:
        total = sum(self.items)
        return self.strategy.pay(total) if self.strategy else ""


if __name__ == "__main__":
    cart = Cart()
    cart.add("商品A", 100)
    cart.strategy = CreditCard("12345678")
    print(cart.checkout())
    cart.strategy = PayPal("a@b.com")
    print(cart.checkout())
