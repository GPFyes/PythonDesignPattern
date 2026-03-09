from abc import ABC, abstractmethod

class Renderer(ABC):
    @abstractmethod
    def render_circle(self, radius): pass
    
    @abstractmethod
    def render_square(self, side): pass

class VectorRenderer(Renderer):
    def render_circle(self, radius):
        return f"向量绘制圆形，半径{radius}"
    
    def render_square(self, side):
        return f"向量绘制正方形，边长{side}"

class RasterRenderer(Renderer):
    def render_circle(self, radius):
        return f"光栅绘制圆形，半径{radius}"
    
    def render_square(self, side):
        return f"光栅绘制正方形，边长{side}"

class Shape(ABC):
    def __init__(self, renderer: Renderer):
        self.renderer = renderer
    
    @abstractmethod
    def draw(self): pass

class Circle(Shape):
    def __init__(self, radius, renderer):
        super().__init__(renderer)
        self.radius = radius
    
    def draw(self):
        return self.renderer.render_circle(self.radius)

class Square(Shape):
    def __init__(self, side, renderer):
        super().__init__(renderer)
        self.side = side
    
    def draw(self):
        return self.renderer.render_square(self.side)

shapes = [
    Circle(10, VectorRenderer()),
    Circle(10, RasterRenderer()),
    Square(5, VectorRenderer()),
    Square(5, RasterRenderer())
]

for s in shapes:
    print(s.draw())
