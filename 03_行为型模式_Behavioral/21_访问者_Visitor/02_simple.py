"""
访问者模式 - 简单级示例
"""

from abc import ABC, abstractmethod
from typing import List


class Shape(ABC):
    @abstractmethod
    def accept(self, visitor: "ShapeVisitor") -> None:
        pass


class Circle(Shape):
    def __init__(self, radius: float):
        self.radius = radius

    def accept(self, visitor: "ShapeVisitor") -> None:
        visitor.visit_circle(self)

    def get_area(self) -> float:
        return 3.14 * self.radius**2


class Rectangle(Shape):
    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height

    def accept(self, visitor: "ShapeVisitor") -> None:
        visitor.visit_rectangle(self)

    def get_area(self) -> float:
        return self.width * self.height


class Triangle(Shape):
    def __init__(self, base: float, height: float):
        self.base = base
        self.height = height

    def accept(self, visitor: "ShapeVisitor") -> None:
        visitor.visit_triangle(self)

    def get_area(self) -> float:
        return 0.5 * self.base * self.height


class ShapeVisitor(ABC):
    @abstractmethod
    def visit_circle(self, circle: Circle) -> None:
        pass

    @abstractmethod
    def visit_rectangle(self, rectangle: Rectangle) -> None:
        pass

    @abstractmethod
    def visit_triangle(self, triangle: Triangle) -> None:
        pass


class AreaCalculator(ShapeVisitor):
    def visit_circle(self, circle: Circle) -> None:
        area = circle.get_area()
        print(f"圆形面积: {area:.2f}")

    def visit_rectangle(self, rectangle: Rectangle) -> None:
        area = rectangle.get_area()
        print(f"矩形面积: {area:.2f}")

    def visit_triangle(self, triangle: Triangle) -> None:
        area = triangle.get_area()
        print(f"三角形面积: {area:.2f}")


class DrawVisitor(ShapeVisitor):
    def visit_circle(self, circle: Circle) -> None:
        print(f"绘制圆形: 半径={circle.radius}")

    def visit_rectangle(self, rectangle: Rectangle) -> None:
        print(f"绘制矩形: 宽={rectangle.width}, 高={rectangle.height}")

    def visit_triangle(self, triangle: Triangle) -> None:
        print(f"绘制三角形: 底={triangle.base}, 高={triangle.height}")


if __name__ == "__main__":
    shapes: List[Shape] = [
        Circle(5),
        Rectangle(4, 6),
        Triangle(3, 4),
    ]

    print("=== 计算面积 ===")
    area_calc = AreaCalculator()
    for shape in shapes:
        shape.accept(area_calc)

    print("\n=== 绘制图形 ===")
    drawer = DrawVisitor()
    for shape in shapes:
        shape.accept(drawer)
