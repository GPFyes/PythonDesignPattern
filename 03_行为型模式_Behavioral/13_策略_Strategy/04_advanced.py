from abc import ABC, abstractmethod
from typing import Dict, List, Optional
from datetime import datetime


class PaymentStrategy(ABC):
    @abstractmethod
    def pay(self, amount: float, context: Dict) -> Dict:
        pass

    @abstractmethod
    def refund(self, transaction_id: str, amount: float) -> Dict:
        pass


class CreditCardPayment(PaymentStrategy):
    def __init__(self, card_number: str, cvv: str, expiry: str):
        self.card_number = card_number
        self.cvv = cvv
        self.expiry = expiry

    def pay(self, amount: float, context: Dict) -> Dict:
        return {
            "status": "success",
            "method": "credit_card",
            "last_four": self.card_number[-4:],
            "amount": amount,
            "timestamp": datetime.now().isoformat()
        }

    def refund(self, transaction_id: str, amount: float) -> Dict:
        return {
            "status": "refunded",
            "method": "credit_card",
            "original_transaction": transaction_id,
            "amount": amount,
            "timestamp": datetime.now().isoformat()
        }


class PayPalPayment(PaymentStrategy):
    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password

    def pay(self, amount: float, context: Dict) -> Dict:
        return {
            "status": "success",
            "method": "paypal",
            "email": self.email,
            "amount": amount,
            "timestamp": datetime.now().isoformat()
        }

    def refund(self, transaction_id: str, amount: float) -> Dict:
        return {
            "status": "refunded",
            "method": "paypal",
            "original_transaction": transaction_id,
            "amount": amount,
            "timestamp": datetime.now().isoformat()
        }


class CryptoPayment(PaymentStrategy):
    def __init__(self, wallet_address: str, network: str):
        self.wallet_address = wallet_address
        self.network = network

    def pay(self, amount: float, context: Dict) -> Dict:
        return {
            "status": "success",
            "method": "cryptocurrency",
            "network": self.network,
            "amount": amount,
            "timestamp": datetime.now().isoformat()
        }

    def refund(self, transaction_id: str, amount: float) -> Dict:
        return {
            "status": "refunded",
            "method": "cryptocurrency",
            "original_transaction": transaction_id,
            "amount": amount,
            "timestamp": datetime.now().isoformat()
        }


class Product:
    def __init__(self, id: str, name: str, price: float):
        self.id = id
        self.name = name
        self.price = price


class CartItem:
    def __init__(self, product: Product, quantity: int):
        self.product = product
        self.quantity = quantity

    def get_total(self) -> float:
        return self.product.price * self.quantity


class ShoppingCart:
    def __init__(self):
        self.items: List[CartItem] = []

    def add_item(self, product: Product, quantity: int = 1):
        for item in self.items:
            if item.product.id == product.id:
                item.quantity += quantity
                return
        self.items.append(CartItem(product, quantity))

    def remove_item(self, product_id: str):
        self.items = [item for item in self.items if item.product.id != product_id]

    def get_total(self) -> float:
        return sum(item.get_total() for item in self.items)

    def clear(self):
        self.items.clear()


class Order:
    def __init__(self, order_id: str, items: List[CartItem], total: float, payment: PaymentStrategy):
        self.order_id = order_id
        self.items = items
        self.total = total
        self.payment = payment
        self.payment_result: Optional[Dict] = None
        self.status = "pending"

    def process_payment(self, context: Dict = None) -> Dict:
        self.payment_result = self.payment.pay(self.total, context or {})
        if self.payment_result["status"] == "success":
            self.status = "paid"
        return self.payment_result


class PaymentProcessor:
    def __init__(self):
        self.payment_strategies: Dict[str, PaymentStrategy] = {}

    def register_strategy(self, name: str, strategy: PaymentStrategy):
        self.payment_strategies[name] = strategy

    def get_strategy(self, name: str) -> PaymentStrategy:
        if name not in self.payment_strategies:
            raise ValueError(f"Payment strategy '{name}' not found")
        return self.payment_strategies[name]

    def process_order(self, order: Order, strategy_name: str, context: Dict = None) -> Dict:
        strategy = self.get_strategy(strategy_name)
        return order.process_payment(context)


if __name__ == "__main__":
    cart = ShoppingCart()
    cart.add_item(Product("P001", "iPhone 15", 6999))
    cart.add_item(Product("P002", "AirPods Pro", 1999))
    cart.add_item(Product("P002", "AirPods Pro", 1))

    print(f"购物车总金额: ¥{cart.get_total()}")

    credit_card = CreditCardPayment("1234567890123456", "123", "12/25")
    paypal = PayPalPayment("user@example.com", "password")
    crypto = CryptoPayment("0xABC123", "Ethereum")

    processor = PaymentProcessor()
    processor.register_strategy("credit_card", credit_card)
    processor.register_strategy("paypal", paypal)
    processor.register_strategy("crypto", crypto)

    order = Order("ORD-001", cart.items, cart.get_total(), credit_card)
    result = processor.process_order(order, "credit_card")
    print(f"\n信用卡支付结果: {result}")

    order2 = Order("ORD-002", cart.items, cart.get_total(), paypal)
    result2 = processor.process_order(order2, "paypal")
    print(f"\nPayPal支付结果: {result2}")
