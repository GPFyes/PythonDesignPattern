"""
解释器模式 - 入门级示例

简介：用最简单的方式演示解释器模式的核心思想
"""


class Expression:
    def interpret(self, context: str) -> bool:
        raise NotImplementedError


class TerminalExpression(Expression):
    def __init__(self, data: str):
        self.data = data

    def interpret(self, context: str) -> bool:
        return self.data in context


class OrExpression(Expression):
    def __init__(self, expr1: Expression, expr2: Expression):
        self.expr1 = expr1
        self.expr2 = expr2

    def interpret(self, context: str) -> bool:
        return self.expr1.interpret(context) or self.expr2.interpret(context)


if __name__ == "__main__":
    is_python = TerminalExpression("Python")
    is_java = TerminalExpression("Java")

    is_python_or_java = OrExpression(is_python, is_java)

    print(f"包含 Python: {is_python_or_java.interpret('I love Python')}")
    print(f"包含 Java: {is_python_or_java.interpret('I love Java')}")
    print(f"包含 Go: {is_python_or_java.interpret('I love Go')}")
