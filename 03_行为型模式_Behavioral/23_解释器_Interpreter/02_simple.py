"""
解释器模式 - 简单级示例
"""

from abc import ABC, abstractmethod


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


if __name__ == "__main__":
    is_python = TerminalExpression("Python")
    is_java = TerminalExpression("Java")
    is_frontend = TerminalExpression("JavaScript")

    python_or_java = OrExpression(is_python, is_java)
    python_and_java = AndExpression(is_python, is_java)

    print("测试 OR 表达式:")
    print(f"  'Python is great': {python_or_java.interpret('Python is great')}")
    print(f"  'Java is great': {python_or_java.interpret('Java is great')}")
    print(f"  'Go is great': {python_or_java.interpret('Go is great')}")

    print("\n测试 AND 表达式:")
    print(f"  'Python and Java': {python_and_java.interpret('Python and Java')}")
    print(f"  'Python only': {python_and_java.interpret('Python only')}")
