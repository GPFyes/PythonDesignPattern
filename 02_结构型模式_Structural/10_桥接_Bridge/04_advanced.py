from abc import ABC, abstractmethod
from typing import List

class Renderer(ABC):
    @abstractmethod
    def render_circle(self, radius): pass
    
    @abstractmethod
    def render_square(self, side): pass
    
    @abstractmethod
    def render_triangle(self, side): pass
    
    @abstractmethod
    def render_line(self, x1, y1, x2, y2): pass
    
    @abstractmethod
    def get_renderer_name(self) -> str: pass

class VectorRenderer(Renderer):
    def render_circle(self, radius):
        return f"[向量渲染器] 绘制圆形 - 半径: {radius}"
    
    def render_square(self, side):
        return f"[向量渲染器] 绘制正方形 - 边长: {side}"
    
    def render_triangle(self, side):
        return f"[向量渲染器] 绘制三角形 - 边长: {side}"
    
    def render_line(self, x1, y1, x2, y2):
        return f"[向量渲染器] 绘制直线 - 从({x1},{y1})到({x2},{y2})"
    
    def get_renderer_name(self):
        return "Vector Renderer"

class RasterRenderer(Renderer):
    def render_circle(self, radius):
        return f"[光栅渲染器] 绘制圆形 - 半径: {radius}"
    
    def render_square(self, side):
        return f"[光栅渲染器] 绘制正方形 - 边长: {side}"
    
    def render_triangle(self, side):
        return f"[光栅渲染器] 绘制三角形 - 边长: {side}"
    
    def render_line(self, x1, y1, x2, y2):
        return f"[光栅渲染器] 绘制直线 - 从({x1},{y1})到({x2},{y2})"
    
    def get_renderer_name(self):
        return "Raster Renderer"

class Shape(ABC):
    def __init__(self, renderer: Renderer):
        self.renderer = renderer
    
    @abstractmethod
    def draw(self) -> str: pass
    
    @abstractmethod
    def resize(self, factor: float) -> None: pass
    
    def get_renderer(self) -> Renderer:
        return self.renderer

class Circle(Shape):
    def __init__(self, radius, renderer):
        super().__init__(renderer)
        self.radius = radius
    
    def draw(self):
        return self.renderer.render_circle(self.radius)
    
    def resize(self, factor):
        self.radius *= factor
    
    def get_info(self):
        return f"Circle(radius={self.radius})"

class Square(Shape):
    def __init__(self, side, renderer):
        super().__init__(renderer)
        self.side = side
    
    def draw(self):
        return self.renderer.render_square(self.side)
    
    def resize(self, factor):
        self.side *= factor
    
    def get_info(self):
        return f"Square(side={self.side})"

class Triangle(Shape):
    def __init__(self, side, renderer):
        super().__init__(renderer)
        self.side = side
    
    def draw(self):
        return self.renderer.render_triangle(self.side)
    
    def resize(self, factor):
        self.side *= factor
    
    def get_info(self):
        return f"Triangle(side={self.side})"

class ShapeCollection:
    def __init__(self):
        self.shapes: List[Shape] = []
    
    def add_shape(self, shape: Shape):
        self.shapes.append(shape)
    
    def draw_all(self):
        results = []
        for shape in self.shapes:
            results.append(shape.draw())
        return results
    
    def resize_all(self, factor: float):
        for shape in self.shapes:
            shape.resize(factor)

vector_renderer = VectorRenderer()
raster_renderer = RasterRenderer()

collection = ShapeCollection()
collection.add_shape(Circle(10, vector_renderer))
collection.add_shape(Circle(10, raster_renderer))
collection.add_shape(Square(5, vector_renderer))
collection.add_shape(Square(5, raster_renderer))
collection.add_shape(Triangle(7, vector_renderer))
collection.add_shape(Triangle(7, raster_renderer))

print("=== 初始绘制 ===")
for result in collection.draw_all():
    print(result)

print("\n=== 缩放后绘制 ===")
collection.resize_all(2)
for result in collection.draw_all():
    print(result)

print("\n=== 渲染器信息 ===")
for shape in collection.shapes:
    print(f"{shape.get_info()} 使用 {shape.get_renderer().get_renderer_name()}")
