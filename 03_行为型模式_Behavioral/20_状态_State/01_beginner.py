"""
State Pattern - Beginner Level
自动售货机入门示例：基本状态转换
"""

from abc import ABC, abstractmethod


class State(ABC):
    @abstractmethod
    def insert_money(self, machine):
        pass

    @abstractmethod
    def select_product(self, machine):
        pass

    @abstractmethod
    def dispense(self, machine):
        pass


class NoMoneyState(State):
    def insert_money(self, machine):
        print("投币成功！")
        machine.set_state(machine.has_money_state)

    def select_product(self, machine):
        print("请先投币！")

    def dispense(self, machine):
        print("请先投币！")


class HasMoneyState(State):
    def insert_money(self, machine):
        print("已投币，请选择商品！")

    def select_product(self, machine):
        print("商品已选择，准备出货...")
        machine.set_state(machine.dispensing_state)

    def dispense(self, machine):
        print("请先选择商品！")


class DispensingState(State):
    def insert_money(self, machine):
        print("正在出货，请稍候...")

    def select_product(self, machine):
        print("正在出货，请稍候...")

    def dispense(self, machine):
        print("出货完成！请取走商品。")
        machine.set_state(machine.no_money_state)


class VendingMachine:
    def __init__(self):
        self.no_money_state = NoMoneyState()
        self.has_money_state = HasMoneyState()
        self.dispensing_state = DispensingState()
        self.current_state = self.no_money_state

    def set_state(self, state):
        self.current_state = state

    def insert_money(self):
        self.current_state.insert_money(self)

    def select_product(self):
        self.current_state.select_product(self)

    def dispense(self):
        self.current_state.dispense(self)


if __name__ == "__main__":
    machine = VendingMachine()

    print("=== 步骤1：直接选择商品 ===")
    machine.select_product()

    print("\n=== 步骤2：投币 ===")
    machine.insert_money()

    print("\n=== 步骤3：再次投币 ===")
    machine.insert_money()

    print("\n=== 步骤4：选择商品 ===")
    machine.select_product()

    print("\n=== 步骤5：出货 ===")
    machine.dispense()

    print("\n=== 步骤6：再次购买 ===")
    machine.insert_money()
    machine.select_product()
    machine.dispense()
