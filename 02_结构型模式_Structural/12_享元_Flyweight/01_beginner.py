class TreeType:
    def __init__(self, name, color, texture):
        self.name = name
        self.color = color
        self.texture = texture

    def draw(self, x, y):
        print(f"在({x},{y})绘制{self.color}{self.name}")


class TreeFactory:
    _types = {}

    @classmethod
    def get_type(cls, name, color, texture):
        key = (name, color, texture)
        if key not in cls._types:
            cls._types[key] = TreeType(name, color, texture)
        return cls._types[key]


class Tree:
    def __init__(self, x, y, name, color, texture):
        self.x = x
        self.y = y
        self.type = TreeFactory.get_type(name, color, texture)

    def draw(self):
        self.type.draw(self.x, self.y)


forest = [Tree(1, 2, "橡树", "绿色", "粗糙"),
          Tree(3, 4, "橡树", "绿色", "粗糙"),
          Tree(5, 6, "松树", "深绿", "光滑")]

for tree in forest:
    tree.draw()
