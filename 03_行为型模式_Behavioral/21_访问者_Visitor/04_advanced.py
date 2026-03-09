"""
访问者模式 - 高级示例

实现一个完整的 AST（抽象语法树）访问者系统
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional


class ASTNode(ABC):
    @abstractmethod
    def accept(self, visitor: "ASTVisitor") -> Any:
        pass


class NumberNode(ASTNode):
    def __init__(self, value: float):
        self.value = value

    def accept(self, visitor: "ASTVisitor") -> Any:
        return visitor.visit_number(self)


class BinaryOpNode(ASTNode):
    def __init__(self, operator: str, left: ASTNode, right: ASTNode):
        self.operator = operator
        self.left = left
        self.right = right

    def accept(self, visitor: "ASTVisitor") -> Any:
        return visitor.visit_binary_op(self)


class UnaryOpNode(ASTNode):
    def __init__(self, operator: str, operand: ASTNode):
        self.operator = operator
        self.operand = operand

    def accept(self, visitor: "ASTVisitor") -> Any:
        return visitor.visit_unary_op(self)


class VariableNode(ASTNode):
    def __init__(self, name: str):
        self.name = name

    def accept(self, visitor: "ASTVisitor") -> Any:
        return visitor.visit_variable(self)


class AssignmentNode(ASTNode):
    def __init__(self, name: str, value: ASTNode):
        self.name = name
        self.value = value

    def accept(self, visitor: "ASTVisitor") -> Any:
        return visitor.visit_assignment(self)


class PrintNode(ASTNode):
    def __init__(self, expr: ASTNode):
        self.expr = expr

    def accept(self, visitor: "ASTVisitor") -> Any:
        return visitor.visit_print(self)


class BlockNode(ASTNode):
    def __init__(self, statements: List[ASTNode]):
        self.statements = statements

    def accept(self, visitor: "ASTVisitor") -> Any:
        return visitor.visit_block(self)


class ASTVisitor(ABC):
    @abstractmethod
    def visit_number(self, node: NumberNode) -> Any:
        pass

    @abstractmethod
    def visit_binary_op(self, node: BinaryOpNode) -> Any:
        pass

    @abstractmethod
    def visit_unary_op(self, node: UnaryOpNode) -> Any:
        pass

    @abstractmethod
    def visit_variable(self, node: VariableNode) -> Any:
        pass

    @abstractmethod
    def visit_assignment(self, node: AssignmentNode) -> Any:
        pass

    @abstractmethod
    def visit_print(self, node: PrintNode) -> Any:
        pass

    @abstractmethod
    def visit_block(self, node: BlockNode) -> Any:
        pass


class ASTEvaluator(ASTVisitor):
    def __init__(self):
        self.variables: Dict[str, float] = {}
        self.output: List[str] = []

    def visit_number(self, node: NumberNode) -> float:
        return node.value

    def visit_binary_op(self, node: BinaryOpNode) -> float:
        left = node.left.accept(self)
        right = node.right.accept(self)

        ops = {
            "+": lambda a, b: a + b,
            "-": lambda a, b: a - b,
            "*": lambda a, b: a * b,
            "/": lambda a, b: a / b if b != 0 else 0,
            "**": lambda a, b: a**b,
        }

        return ops.get(node.operator, lambda a, b: 0)(left, right)

    def visit_unary_op(self, node: UnaryOpNode) -> float:
        operand = node.operand.accept(self)

        if node.operator == "-":
            return -operand
        elif node.operator == "+":
            return operand

        return 0

    def visit_variable(self, node: VariableNode) -> float:
        if node.name not in self.variables:
            raise NameError(f"未定义的变量: {node.name}")
        return self.variables[node.name]

    def visit_assignment(self, node: AssignmentNode) -> float:
        value = node.value.accept(self)
        self.variables[node.name] = value
        return value

    def visit_print(self, node: PrintNode) -> Any:
        value = node.expr.accept(self)
        self.output.append(str(value))
        print(f"打印: {value}")
        return None

    def visit_block(self, node: BlockNode) -> Any:
        result = None
        for stmt in node.statements:
            result = stmt.accept(self)
        return result


class ASTPrinter(ASTVisitor):
    def visit_number(self, node: NumberNode) -> str:
        return str(node.value)

    def visit_binary_op(self, node: BinaryOpNode) -> str:
        left = node.left.accept(self)
        right = node.right.accept(self)
        return f"({left} {node.operator} {right})"

    def visit_unary_op(self, node: UnaryOpNode) -> str:
        operand = node.operand.accept(self)
        return f"({node.operator}{operand})"

    def visit_variable(self, node: VariableNode) -> str:
        return node.name

    def visit_assignment(self, node: AssignmentNode) -> str:
        value = node.value.accept(self)
        return f"{node.name} = {value}"

    def visit_print(self, node: PrintNode) -> str:
        expr = node.expr.accept(self)
        return f"print({expr})"

    def visit_block(self, node: BlockNode) -> str:
        statements = [stmt.accept(self) for stmt in node.statements]
        return "{\n  " + "\n  ".join(statements) + "\n}"


class ASTAnalyzer(ASTVisitor):
    def __init__(self):
        self.variables: set = set()
        self.used_variables: set = set()
        self.defined_variables: set = set()

    def visit_number(self, node: NumberNode) -> None:
        pass

    def visit_binary_op(self, node: BinaryOpNode) -> None:
        node.left.accept(self)
        node.right.accept(self)

    def visit_unary_op(self, node: UnaryOpNode) -> None:
        node.operand.accept(self)

    def visit_variable(self, node: VariableNode) -> None:
        self.used_variables.add(node.name)

    def visit_assignment(self, node: AssignmentNode) -> None:
        self.defined_variables.add(node.name)
        node.value.accept(self)

    def visit_print(self, node: PrintNode) -> None:
        node.expr.accept(self)

    def visit_block(self, node: BlockNode) -> None:
        for stmt in node.statements:
            stmt.accept(self)


def demo_expression_evaluation():
    print("=== 表达式求值 ===")

    expr = BinaryOpNode(
        "+", BinaryOpNode("*", NumberNode(2), NumberNode(3)), NumberNode(1)
    )

    evaluator = ASTEvaluator()
    result = expr.accept(evaluator)
    print(f"(2 * 3) + 1 = {result}")


def demo_variable_assignment():
    print("\n=== 变量赋值 ===")

    program = BlockNode(
        [
            AssignmentNode("x", NumberNode(10)),
            AssignmentNode("y", BinaryOpNode("*", VariableNode("x"), NumberNode(2))),
            PrintNode(VariableNode("y")),
            AssignmentNode(
                "z", BinaryOpNode("+", VariableNode("x"), VariableNode("y"))
            ),
            PrintNode(VariableNode("z")),
        ]
    )

    evaluator = ASTEvaluator()
    program.accept(evaluator)

    print(f"\n变量表: {evaluator.variables}")


def demo_ast_printer():
    print("\n=== AST 打印 ===")

    expr = BinaryOpNode(
        "+", BinaryOpNode("*", NumberNode(2), VariableNode("x")), NumberNode(1)
    )

    printer = ASTPrinter()
    ast_str = expr.accept(printer)
    print(f"AST: {ast_str}")


def demo_code_analysis():
    print("\n=== 代码分析 ===")

    program = BlockNode(
        [
            AssignmentNode("x", NumberNode(5)),
            AssignmentNode("y", NumberNode(10)),
            PrintNode(BinaryOpNode("+", VariableNode("x"), VariableNode("z"))),
        ]
    )

    analyzer = ASTAnalyzer()
    program.accept(analyzer)

    print(f"定义的变量: {analyzer.defined_variables}")
    print(f"使用的变量: {analyzer.used_variables}")
    print(f"未定义的变量: {analyzer.used_variables - analyzer.defined_variables}")


def demo_complex_expression():
    print("\n=== 复杂表达式 ===")

    expr = BinaryOpNode(
        "**", BinaryOpNode("+", NumberNode(1), NumberNode(2)), NumberNode(3)
    )

    evaluator = ASTEvaluator()
    result = expr.accept(evaluator)
    print(f"(1 + 2) ** 3 = {result}")


if __name__ == "__main__":
    demo_expression_evaluation()
    demo_variable_assignment()
    demo_ast_printer()
    demo_code_analysis()
    demo_complex_expression()
