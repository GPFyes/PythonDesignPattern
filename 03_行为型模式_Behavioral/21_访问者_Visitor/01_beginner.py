"""
访问者模式 - 入门级示例

简介：用最简单的方式演示访问者模式的核心思想
"""


class Element:
    def accept(self, visitor):
        pass


class ConcreteElementA(Element):
    def __init__(self, data: str):
        self.data = data

    def accept(self, visitor):
        visitor.visit_concrete_element_a(self)


class ConcreteElementB(Element):
    def __init__(self, value: int):
        self.value = value

    def accept(self, visitor):
        visitor.visit_concrete_element_b(self)


class Visitor:
    def visit_concrete_element_a(self, element):
        pass

    def visit_concrete_element_b(self, element):
        pass


class ConcreteVisitor(Visitor):
    def visit_concrete_element_a(self, element):
        print(f"访问者处理 ElementA: {element.data}")

    def visit_concrete_element_b(self, element):
        print(f"访问者处理 ElementB: {element.value}")


if __name__ == "__main__":
    elements = [
        ConcreteElementA("Hello"),
        ConcreteElementB(100),
        ConcreteElementA("World"),
        ConcreteElementB(200),
    ]

    visitor = ConcreteVisitor()

    for element in elements:
        element.accept(visitor)
