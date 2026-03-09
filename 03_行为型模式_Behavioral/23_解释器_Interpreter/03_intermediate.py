"""
解释器模式 - 中级示例
实现一个简单的正则表达式解释器
"""

from abc import ABC, abstractmethod
from typing import Dict


class Expression(ABC):
    @abstractmethod
    def interpret(self, context: str) -> bool:
        pass


class TerminalExpression(Expression):
    def __init__(self, data: str):
        self.data = data

    def interpret(self, context: str) -> bool:
        return self.data in context


class OrExpression(Expression):
    def __init__(self, left: Expression, right: Expression):
        self.left = left
        self.right = right

    def interpret(self, context: str) -> bool:
        return self.left.interpret(context) or self.right.interpret(context)


class AndExpression(Expression):
    def __init__(self, left: Expression, right: Expression):
        self.left = left
        self.right = right

    def interpret(self, context: str) -> bool:
        return self.left.interpret(context) and self.right.interpret(context)


class NotExpression(Expression):
    def __init__(self, expr: Expression):
        self.expr = expr

    def interpret(self, context: str) -> bool:
        return not self.expr.interpret(context)


class NumberExpression(Expression):
    def __init__(self, min_val: int, max_val: int):
        self.min_val = min_val
        self.max_val = max_val

    def interpret(self, context: str) -> bool:
        try:
            num = int(context)
            return self.min_val <= num <= self.max_val
        except ValueError:
            return False


class Context:
    def __init__(self):
        self.variables: Dict[str, bool] = {}

    def set(self, key: str, value: bool) -> None:
        self.variables[key] = value

    def get(self, key: str) -> bool:
        return self.variables.get(key, False)


class VariableExpression(Expression):
    def __init__(self, name: str):
        self.name = name

    def interpret(self, context: str) -> bool:
        ctx = Context()
        if self.name in ctx.variables:
            return ctx.variables[self.name]
        return False


if __name__ == "__main__":
    print("=== 测试基本解释器 ===")

    has_python = TerminalExpression("Python")
    has_java = TerminalExpression("Java")
    has_go = TerminalExpression("Go")

    java_or_go = OrExpression(has_java, has_go)
    python_and_java = AndExpression(has_python, has_java)

    print(f"Python OR Java, context='Python': {python_and_java.interpret('Python')}")

    not_java = NotExpression(has_java)
    print(f"NOT Java, context='Python': {not_java.interpret('Python')}")
    print(f"NOT Java, context='Java': {not_java.interpret('Java')}")

    print("\n=== 测试数字范围 ===")
    number_1_to_100 = NumberExpression(1, 100)
    print(f"50 在 1-100 之间: {number_1_to_100.interpret('50')}")
    print(f"150 在 1-100 之间: {number_1_to_100.interpret('150')}")
    print(f"abc 在 1-100 之间: {number_1_to_100.interpret('abc')}")
