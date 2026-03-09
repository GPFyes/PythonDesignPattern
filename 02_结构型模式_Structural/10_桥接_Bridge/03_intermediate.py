from abc import ABC, abstractmethod

class Renderer(ABC):
    @abstractmethod
    def render_circle(self, radius): pass
    
    @abstractmethod
    def render_square(self, side): pass
    
    @abstractmethod
    def render_triangle(self, side): pass

class VectorRenderer(Renderer):
    def render_circle(self, radius):
        return f"[向量] 绘制圆形，半径={radius}"
    
    def render_square(self, side):
        return f"[向量] 绘制正方形，边长={side}"
    
    def render_triangle(self, side):
        return f"[向量] 绘制三角形，边长={side}"

class RasterRenderer(Renderer):
    def render_circle(self, radius):
        return f"[光栅] 绘制圆形，半径={radius}"
    
    def render_square(self, side):
        return f"[光栅] 绘制正方形，边长={side}"
    
    def render_triangle(self, side):
        return f"[光栅] 绘制三角形，边长={side}"

class Shape(ABC):
    def __init__(self, renderer: Renderer):
        self.renderer = renderer
    
    @abstractmethod
    def draw(self) -> str: pass
    
    @abstractmethod
    def resize(self, factor: float) -> None: pass

class Circle(Shape):
    def __init__(self, radius, renderer):
        super().__init__(renderer)
        self.radius = radius
    
    def draw(self):
        return self.renderer.render_circle(self.radius)
    
    def resize(self, factor):
        self.radius *= factor

class Square(Shape):
    def __init__(self, side, renderer):
        super().__init__(renderer)
        self.side = side
    
    def draw(self):
        return self.renderer.render_square(self.side)
    
    def resize(self, factor):
        self.side *= factor

class Triangle(Shape):
    def __init__(self, side, renderer):
        super().__init__(renderer)
        self.side = side
    
    def draw(self):
        return self.renderer.render_triangle(self.side)
    
    def resize(self, factor):
        self.side *= factor

def draw_shapes(shapes):
    for shape in shapes:
        print(shape.draw())

shapes = [
    Circle(10, VectorRenderer()),
    Circle(10, RasterRenderer()),
    Square(5, VectorRenderer()),
    Square(5, RasterRenderer()),
    Triangle(7, VectorRenderer()),
    Triangle(7, RasterRenderer())
]

draw_shapes(shapes)
