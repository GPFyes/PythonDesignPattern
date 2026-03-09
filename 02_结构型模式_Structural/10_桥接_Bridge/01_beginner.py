class Renderer:
    def render_circle(self, radius): pass

class VectorRenderer(Renderer):
    def render_circle(self, radius):
        return f"绘制向量圆形，半径{radius}"

class RasterRenderer(Renderer):
    def render_circle(self, radius):
        return f"绘制光栅圆形，半径{radius}"

class Circle:
    def __init__(self, radius, renderer):
        self.radius = radius
        self.renderer = renderer
    
    def draw(self):
        return self.renderer.render_circle(self.radius)

c1 = Circle(5, VectorRenderer())
c2 = Circle(5, RasterRenderer())
print(c1.draw())
print(c2.draw())
