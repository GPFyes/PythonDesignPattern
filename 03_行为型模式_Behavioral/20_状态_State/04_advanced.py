"""
State Pattern - Advanced Level
自动售货机高级示例：完整功能版，支持状态历史、观察者模式、状态机配置
"""

from abc import ABC, abstractmethod
from enum import Enum
from datetime import datetime
from typing import Dict, List, Callable
import time
import random


class Product(Enum):
    COLA = ("可乐", 3, 10)
    CHIPS = ("薯片", 5, 8)
    WATER = ("矿泉水", 2, 15)
    CANDY = ("糖果", 1, 20)
    TEA = ("绿茶", 4, 12)

    def __init__(self, name, price, stock):
        self.name = name
        self.price = price
        self.stock = stock


class PaymentMethod(Enum):
    CASH = "现金"
    WECHAT = "微信"
    ALIPAY = "支付宝"
    IC_CARD = "IC卡"


class Event:
    def __init__(self, event_type: str, data: dict):
        self.event_type = event_type
        self.data = data
        self.timestamp = datetime.now()


class Observer(ABC):
    @abstractmethod
    def update(self, event: Event):
        pass


class StateMachine(ABC):
    @abstractmethod
    def handle(self, machine, event: Event) -> bool:
        pass
    
    @abstractmethod
    def get_state_name(self) -> str:
        pass


class NoMoneyState(StateMachine):
    def handle(self, machine, event: Event) -> bool:
        if event.event_type == "INSERT_MONEY":
            amount = event.data.get("amount", 0)
            method = event.data.get("method", PaymentMethod.CASH)
            if amount > 0:
                machine.add_money(amount)
                machine.set_payment_method(method)
                print(f"[{self.get_state_name()}] 投币：{amount}元，方式：{method.value}")
                machine.set_state(machine.has_money_state)
                machine.notify_observers(Event("MONEY_INSERTED", {"amount": amount}))
                return True
        elif event.event_type == "CHECK_STATUS":
            print(f"[{self.get_state_name()}] 当前状态：等待投币")
            return True
        return False

    def get_state_name(self) -> str:
        return "NoMoneyState"


class HasMoneyState(StateMachine):
    def handle(self, machine, event: Event) -> bool:
        if event.event_type == "INSERT_MONEY":
            amount = event.data.get("amount", 0)
            if amount > 0:
                machine.add_money(amount)
                print(f"[{self.get_state_name()}] 继续投币：{amount}元，总计：{machine.total_money}元")
                machine.notify_observers(Event("MONEY_INSERTED", {"amount": amount}))
                return True
        elif event.event_type == "SELECT_PRODUCT":
            product = event.data.get("product")
            return self._process_purchase(machine, product)
        elif event.event_type == "CANCEL":
            print(f"[{self.get_state_name()}] 交易取消，退款：{machine.total_money}元")
            machine.set_money(0)
            machine.set_payment_method(None)
            machine.set_state(machine.no_money_state)
            machine.notify_observers(Event("TRANSACTION_CANCELLED", {}))
            return True
        elif event.event_type == "CHECK_STATUS":
            print(f"[{self.get_state_name()}] 当前状态：已投币 {machine.total_money}元")
            return True
        return False

    def _process_purchase(self, machine, product):
        price = machine.get_discounted_price(product)
        
        if machine.get_stock(product) <= 0:
            print(f"[{self.get_state_name()}] {product.value.name} 已售罄！")
            machine.notify_observers(Event("OUT_OF_STOCK", {"product": product.value.name}))
            return False
        
        if machine.total_money < price:
            print(f"[{self.get_state_name()}] 金额不足，需要{price}元，当前{machine.total_money}元")
            return False
        
        machine.deduct_stock(product)
        change = machine.total_money - price
        machine.add_sales(price)
        
        print(f"[{self.get_state_name()}] 出货：{product.value.name}，价格：{price}元")
        if change > 0:
            print(f"[{self.get_state_name()}] 找零：{change}元")
        
        machine.set_money(0)
        machine.set_payment_method(None)
        machine.set_state(machine.no_money_state)
        
        machine.notify_observers(Event("PURCHASE_COMPLETED", {
            "product": product.value.name,
            "price": price,
            "change": change
        }))
        return True

    def get_state_name(self) -> str:
        return "HasMoneyState"


class MaintenanceState(StateMachine):
    def handle(self, machine, event: Event) -> bool:
        if event.event_type == "EXIT_MAINTENANCE":
            print(f"[{self.get_state_name()}] 退出维护模式")
            machine.set_state(machine.no_money_state)
            machine.notify_observers(Event("EXITED_MAINTENANCE", {}))
            return True
        elif event.event_type == "CHECK_STATUS":
            print(f"[{self.get_state_name()}] 当前状态：维护中")
            return True
        elif event.event_type == "REFILL_STOCK":
            product = event.data.get("product")
            quantity = event.data.get("quantity", 10)
            machine.add_stock(product, quantity)
            print(f"[{self.get_state_name()}] 补货：{product.value.name} x {quantity}")
            machine.notify_observers(Event("STOCK_REFILLED", {"product": product.value.name, "quantity": quantity}))
            return True
        return False

    def get_state_name(self) -> str:
        return "MaintenanceState"


class VendingMachine:
    def __init__(self):
        self.no_money_state = NoMoneyState()
        self.has_money_state = HasMoneyState()
        self.maintenance_state = MaintenanceState()
        
        self.current_state = self.no_money_state
        self.total_money = 0
        self.payment_method = None
        self.stock: Dict[Product, int] = {p: p.value.stock for p in Product}
        self.sales = 0
        self.transaction_count = 0
        self.promotion_active = False
        self.promotion_discount = 1.0
        self.observers: List[Observer] = []
        self.state_history: List[str] = []
        self.error_count = 0

    def set_state(self, state):
        self.current_state = state
        self.state_history.append(state.get_state_name())
        if len(self.state_history) > 10:
            self.state_history.pop(0)

    def add_money(self, amount):
        self.total_money += amount

    def set_money(self, amount):
        self.total_money = amount

    def set_payment_method(self, method):
        self.payment_method = method

    def get_stock(self, product):
        return self.stock.get(product, 0)

    def add_stock(self, product, quantity):
        self.stock[product] = self.stock.get(product, 0) + quantity

    def deduct_stock(self, product):
        if product in self.stock:
            self.stock[product] -= 1

    def get_discounted_price(self, product):
        price = product.value.price
        if self.promotion_active:
            price = int(price * self.promotion_discount)
        if self.payment_method in [PaymentMethod.WECHAT, PaymentMethod.ALIPAY]:
            price = int(price * 0.95)
        return price

    def add_sales(self, amount):
        self.sales += amount
        self.transaction_count += 1

    def activate_promotion(self, discount: float = 0.8):
        self.promotion_active = True
        self.promotion_discount = discount
        print(f"[VendingMachine] 促销活动开启：{discount*100}%")

    def deactivate_promotion(self):
        self.promotion_active = False
        self.promotion_discount = 1.0
        print(f"[VendingMachine] 促销活动结束")

    def enter_maintenance(self):
        print(f"[VendingMachine] 进入维护模式")
        self.set_state(self.maintenance_state)
        self.notify_observers(Event("ENTERED_MAINTENANCE", {}))

    def send_event(self, event: Event) -> bool:
        try:
            result = self.current_state.handle(self, event)
            if not result:
                print(f"[VendingMachine] 事件 {event.event_type} 未被处理")
                self.error_count += 1
            return result
        except Exception as e:
            print(f"[VendingMachine] 处理事件出错：{e}")
            self.error_count += 1
            return False

    def add_observer(self, observer: Observer):
        self.observers.append(observer)

    def remove_observer(self, observer: Observer):
        self.observers.remove(observer)

    def notify_observers(self, event: Event):
        for observer in self.observers:
            try:
                observer.update(event)
            except Exception as e:
                print(f"[VendingMachine] 通知观察者出错：{e}")

    def get_status(self) -> dict:
        return {
            "current_state": self.current_state.get_state_name(),
            "total_money": self.total_money,
            "payment_method": self.payment_method.value if self.payment_method else None,
            "sales": self.sales,
            "transaction_count": self.transaction_count,
            "stock": {p.value.name: count for p, count in self.stock.items()},
            "promotion_active": self.promotion_active,
            "error_count": self.error_count,
            "state_history": self.state_history
        }

    def show_info(self):
        status = self.get_status()
        print(f"\n{'='*50}")
        print(f"自动售货机状态")
        print(f"{'='*50}")
        print(f"当前状态：{status['current_state']}")
        print(f"当前金额：{status['total_money']}元")
        print(f"支付方式：{status['payment_method'] or '无'}")
        print(f"总销售额：{status['sales']}元")
        print(f"交易次数：{status['transaction_count']}")
        print(f"促销状态：{'开启' if status['promotion_active'] else '关闭'}")
        print(f"异常次数：{status['error_count']}")
        print(f"状态历史：{status['state_history']}")
        
        print(f"\n商品库存：")
        for product in Product:
            stock = self.get_stock(product)
            price = self.get_discounted_price(product)
            status_str = "充足" if stock > 5 else "不足" if stock > 0 else "售罄"
            print(f"  {product.value.name}: {stock}件, {price}元 [{status_str}]")
        print(f"{'='*50}\n")


class SalesLogger(Observer):
    def update(self, event: Event):
        if event.event_type == "PURCHASE_COMPLETED":
            print(f"[销售日志] 购买成功：{event.data['product']}, 金额：{event.data['price']}元")
        elif event.event_type == "TRANSACTION_CANCELLED":
            print(f"[销售日志] 交易取消")


class StockMonitor(Observer):
    def update(self, event: Event):
        if event.event_type == "OUT_OF_STOCK":
            print(f"[库存警告] {event.data['product']} 已售罄！需要补货！")
        elif event.event_type == "STOCK_REFILLED":
            print(f"[库存通知] {event.data['product']} 已补货，当前库存：{event.data['quantity']}")


class MaintenanceLogger(Observer):
    def update(self, event: Event):
        if event.event_type in ["ENTERED_MAINTENANCE", "EXITED_MAINTENANCE"]:
            print(f"[维护日志] 维护模式：{event.event_type}")


def main():
    print("=" * 60)
    print("自动售货机系统 - 高级示例")
    print("=" * 60)

    machine = VendingMachine()
    
    machine.add_observer(SalesLogger())
    machine.add_observer(StockMonitor())
    machine.add_observer(MaintenanceLogger())

    machine.show_info()

    print("\n>>> 场景1：正常购买流程")
    machine.send_event(Event("INSERT_MONEY", {"amount": 5, "method": PaymentMethod.WECHAT}))
    machine.send_event(Event("SELECT_PRODUCT", {"product": Product.COLA}))
    machine.send_event(Event("CHECK_STATUS", {}))

    print("\n>>> 场景2：投币不足")
    machine.send_event(Event("INSERT_MONEY", {"amount": 2, "method": PaymentMethod.CASH}))
    machine.send_event(Event("SELECT_PRODUCT", {"product": Product.CHIPS}))

    print("\n>>> 场景3：取消交易")
    machine.send_event(Event("INSERT_MONEY", {"amount": 10, "method": PaymentMethod.ALIPAY}))
    machine.send_event(Event("CANCEL", {}))

    print("\n>>> 场景4：促销活动")
    machine.activate_promotion(0.8)
    machine.send_event(Event("INSERT_MONEY", {"amount": 5, "method": PaymentMethod.WECHAT}))
    machine.send_event(Event("SELECT_PRODUCT", {"product": Product.TEA}))

    print("\n>>> 场景5：进入维护模式")
    machine.enter_maintenance()
    machine.send_event(Event("REFILL_STOCK", {"product": Product.COLA, "quantity": 20}))
    machine.send_event(Event("EXIT_MAINTENANCE", {}))

    print("\n>>> 场景6：购买多个商品（测试库存）")
    for _ in range(3):
        machine.send_event(Event("INSERT_MONEY", {"amount": 5, "method": PaymentMethod.CASH}))
        machine.send_event(Event("SELECT_PRODUCT", {"product": Product.WATER}))

    machine.show_info()

    print("\n>>> 场景7：测试错误处理")
    machine.send_event(Event("UNKNOWN_EVENT", {}))

    machine.show_info()


if __name__ == "__main__":
    main()
