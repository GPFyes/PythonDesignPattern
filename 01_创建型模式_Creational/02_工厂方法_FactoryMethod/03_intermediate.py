"""
工厂方法模式 - 中级示例

简介：结合实际场景，展示简单计算器的应用
"""

from abc import ABC, abstractmethod
from typing import Union


class Operation(ABC):
    """
    运算抽象类（产品角色）
    
    定义运算操作的统一接口
    """
    
    @abstractmethod
    def calculate(self, a: float, b: float) -> float:
        """
        执行计算
        
        Args:
            a: 第一个操作数
            b: 第二个操作数
        
        Returns:
            计算结果
        """
        pass
    
    @abstractmethod
    def get_symbol(self) -> str:
        """获取运算符号"""
        pass


class AddOperation(Operation):
    """加法运算"""
    
    def calculate(self, a: float, b: float) -> float:
        return a + b
    
    def get_symbol(self) -> str:
        return "+"


class SubtractOperation(Operation):
    """减法运算"""
    
    def calculate(self, a: float, b: float) -> float:
        return a - b
    
    def get_symbol(self) -> str:
        return "-"


class MultiplyOperation(Operation):
    """乘法运算"""
    
    def calculate(self, a: float, b: float) -> float:
        return a * b
    
    def get_symbol(self) -> str:
        return "*"


class DivideOperation(Operation):
    """除法运算"""
    
    def calculate(self, a: float, b: float) -> float:
        if b == 0:
            raise ValueError("除数不能为零")
        return a / b
    
    def get_symbol(self) -> str:
        return "/"


class OperationFactory(ABC):
    """
    运算工厂抽象类（创建者角色）
    
    声明创建运算对象的工厂方法
    """
    
    @abstractmethod
    def create_operation(self) -> Operation:
        """创建运算对象的工厂方法"""
        pass


class AddFactory(OperationFactory):
    """加法工厂"""
    
    def create_operation(self) -> Operation:
        return AddOperation()


class SubtractFactory(OperationFactory):
    """减法工厂"""
    
    def create_operation(self) -> Operation:
        return SubtractOperation()


class MultiplyFactory(OperationFactory):
    """乘法工厂"""
    
    def create_operation(self) -> Operation:
        return MultiplyOperation()


class DivideFactory(OperationFactory):
    """除法工厂"""
    
    def create_operation(self) -> Operation:
        return DivideOperation()


class Calculator:
    """
    计算器类
    
    使用工厂方法创建运算对象
    """
    
    def __init__(self, factory: OperationFactory):
        """初始化计算器，传入工厂"""
        self.operation = factory.create_operation()
    
    def calculate(self, a: float, b: float) -> float:
        """执行计算"""
        result = self.operation.calculate(a, b)
        symbol = self.operation.get_symbol()
        print(f"{a} {symbol} {b} = {result}")
        return result


def main():
    """测试工厂方法模式 - 计算器"""
    print("=" * 50)
    print("工厂方法模式 - 简单计算器")
    print("=" * 50)
    
    # 使用加法
    add_calculator = Calculator(AddFactory())
    add_calculator.calculate(10, 5)
    
    # 使用减法
    sub_calculator = Calculator(SubtractFactory())
    sub_calculator.calculate(10, 5)
    
    # 使用乘法
    mul_calculator = Calculator(MultiplyFactory())
    mul_calculator.calculate(10, 5)
    
    # 使用除法
    div_calculator = Calculator(DivideFactory())
    div_calculator.calculate(10, 5)
    
    print("\n说明：")
    print("- 每种运算对应一个工厂")
    print("- 新增运算只需添加新的工厂和产品类")
    print("- 符合开闭原则")


if __name__ == "__main__":
    main()
