"""
解释器模式 - 高级示例

实现一个完整的数学表达式解释器，支持加减乘除和变量
"""

from abc import ABC, abstractmethod
from typing import Dict, Optional
import re


class Expression(ABC):
    @abstractmethod
    def interpret(self, variables: Dict[str, float]) -> float:
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass


class NumberExpression(Expression):
    def __init__(self, number: float):
        self.number = number

    def interpret(self, variables: Dict[str, float]) -> float:
        return self.number

    def __str__(self) -> str:
        return str(self.number)


class VariableExpression(Expression):
    def __init__(self, name: str):
        self.name = name

    def interpret(self, variables: Dict[str, float]) -> float:
        if self.name not in variables:
            raise ValueError(f"未定义的变量: {self.name}")
        return variables[self.name]

    def __str__(self) -> str:
        return self.name


class AddExpression(Expression):
    def __init__(self, left: Expression, right: Expression):
        self.left = left
        self.right = right

    def interpret(self, variables: Dict[str, float]) -> float:
        return self.left.interpret(variables) + self.right.interpret(variables)

    def __str__(self) -> str:
        return f"({self.left} + {self.right})"


class SubtractExpression(Expression):
    def __init__(self, left: Expression, right: Expression):
        self.left = left
        self.right = right

    def interpret(self, variables: Dict[str, float]) -> float:
        return self.left.interpret(variables) - self.right.interpret(variables)

    def __str__(self) -> str:
        return f"({self.left} - {self.right})"


class MultiplyExpression(Expression):
    def __init__(self, left: Expression, right: Expression):
        self.left = left
        self.right = right

    def interpret(self, variables: Dict[str, float]) -> float:
        return self.left.interpret(variables) * self.right.interpret(variables)

    def __str__(self) -> str:
        return f"({self.left} * {self.right})"


class DivideExpression(Expression):
    def __init__(self, left: Expression, right: Expression):
        self.left = left
        self.right = right

    def interpret(self, variables: Dict[str, float]) -> float:
        divisor = self.right.interpret(variables)
        if divisor == 0:
            raise ValueError("除数不能为零")
        return self.left.interpret(variables) / divisor

    def __str__(self) -> str:
        return f"({self.left} / {self.right})"


class Parser:
    def __init__(self, expression: str):
        self.expression = expression.replace(" ", "")
        self.pos = 0

    def parse(self) -> Expression:
        result = self.parse_add_sub()
        if self.pos != len(self.expression):
            raise ValueError(f"解析错误: 剩余字符 '{self.expression[self.pos :]}'")
        return result

    def parse_add_sub(self) -> Expression:
        left = self.parse_mul_div()

        while self.pos < len(self.expression) and self.expression[self.pos] in "+-":
            op = self.expression[self.pos]
            self.pos += 1
            right = self.parse_mul_div()

            if op == "+":
                left = AddExpression(left, right)
            else:
                left = SubtractExpression(left, right)

        return left

    def parse_mul_div(self) -> Expression:
        left = self.parse_primary()

        while self.pos < len(self.expression) and self.expression[self.pos] in "*/":
            op = self.expression[self.pos]
            self.pos += 1
            right = self.parse_primary()

            if op == "*":
                left = MultiplyExpression(left, right)
            else:
                left = DivideExpression(left, right)

        return left

    def parse_primary(self) -> Expression:
        if self.expression[self.pos] == "(":
            self.pos += 1
            expr = self.parse_add_sub()
            if self.pos >= len(self.expression) or self.expression[self.pos] != ")":
                raise ValueError("缺少右括号")
            self.pos += 1
            return expr

        if self.expression[self.pos].isalpha():
            start = self.pos
            while (
                self.pos < len(self.expression) and self.expression[self.pos].isalnum()
            ):
                self.pos += 1
            return VariableExpression(self.expression[start : self.pos])

        start = self.pos
        while self.pos < len(self.expression) and (
            self.expression[self.pos].isdigit() or self.expression[self.pos] == "."
        ):
            self.pos += 1
        return NumberExpression(float(self.expression[start : self.pos]))


class Calculator:
    def __init__(self):
        self.variables: Dict[str, float] = {}
        self.history: list = []

    def set_variable(self, name: str, value: float) -> None:
        self.variables[name] = value

    def evaluate(self, expression: str) -> float:
        parser = Parser(expression)
        expr = parser.parse()
        result = expr.interpret(self.variables)
        self.history.append(
            {
                "expression": expression,
                "result": result,
                "variables": self.variables.copy(),
            }
        )
        return result

    def get_history(self) -> list:
        return self.history

    def clear_history(self) -> None:
        self.history.clear()


def demo_basic_expressions():
    print("=== 基本表达式测试 ===")
    calc = Calculator()

    expressions = [
        "10 + 5",
        "10 - 5",
        "10 * 5",
        "10 / 5",
        "2 + 3 * 4",
        "(2 + 3) * 4",
    ]

    for expr in expressions:
        result = calc.evaluate(expr)
        print(f"{expr} = {result}")


def demo_variables():
    print("\n=== 变量测试 ===")
    calc = Calculator()

    calc.set_variable("x", 10)
    calc.set_variable("y", 5)

    expressions = [
        "x + y",
        "x - y",
        "x * y",
        "x / y",
        "x + y * 2",
        "(x + y) * 2",
    ]

    for expr in expressions:
        result = calc.evaluate(expr)
        print(f"{expr} = {result}")


def demo_complex():
    print("\n=== 复杂表达式测试 ===")
    calc = Calculator()

    calc.set_variable("a", 100)
    calc.set_variable("b", 20)
    calc.set_variable("c", 5)

    expr = "(a + b) * c"
    result = calc.evaluate(expr)
    print(f"{expr} = {result}")

    expr = "a + b * c"
    result = calc.evaluate(expr)
    print(f"{expr} = {result}")


def demo_error_handling():
    print("\n=== 错误处理测试 ===")
    calc = Calculator()
    calc.set_variable("x", 10)

    try:
        calc.evaluate("x + y")
    except ValueError as e:
        print(f"错误捕获: {e}")

    try:
        calc.evaluate("10 / 0")
    except ValueError as e:
        print(f"错误捕获: {e}")


if __name__ == "__main__":
    demo_basic_expressions()
    demo_variables()
    demo_complex()
    demo_error_handling()

    print("\n=== 计算历史 ===")
    calc = Calculator()
    calc.set_variable("a", 10)
    calc.set_variable("b", 5)
    calc.evaluate("a + b")
    calc.evaluate("a - b")
    calc.evaluate("a * b")

    for item in calc.get_history():
        print(f"  {item['expression']} = {item['result']}")
