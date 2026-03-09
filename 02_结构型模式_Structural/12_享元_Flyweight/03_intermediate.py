from abc import ABC, abstractmethod
import random


class TreeType(ABC):
    @abstractmethod
    def draw(self, canvas, x, y):
        pass

    @abstractmethod
    def get_info(self):
        pass


class ConcreteTreeType(TreeType):
    def __init__(self, name, color, texture, foliage_type):
        self.name = name
        self.color = color
        self.texture = texture
        self.foliage_type = foliage_type

    def draw(self, canvas, x, y):
        print(f"[{canvas}] 在位置({x},{y})绘制{self.color}{self.name}({self.foliage_type})")

    def get_info(self):
        return f"树木类型:{self.name}, 颜色:{self.color}, 纹理:{self.texture}"


class TreeFactory:
    _tree_types = {}

    @classmethod
    def get_tree_type(cls, name, color, texture, foliage_type):
        key = (name, color, texture, foliage_type)
        if key not in cls._tree_types:
            cls._tree_types[key] = ConcreteTreeType(name, color, texture, foliage_type)
            print(f"创建新树木类型:{name}")
        return cls._tree_types[key]

    @classmethod
    def get_type_count(cls):
        return len(cls._tree_types)


class Tree:
    def __init__(self, x, y, name, color, texture, foliage_type):
        self.x = x
        self.y = y
        self.type = TreeFactory.get_tree_type(name, color, texture, foliage_type)

    def draw(self, canvas="画布"):
        self.type.draw(canvas, self.x, self.y)

    def get_type_info(self):
        return self.type.get_info()


class Forest:
    def __init__(self):
        self.trees = []

    def plant_tree(self, x, y, name, color, texture, foliage_type):
        tree = Tree(x, y, name, color, texture, foliage_type)
        self.trees.append(tree)

    def draw_all(self, canvas="画布"):
        print(f"\n=== 开始绘制森林 (共{len(self.trees)}棵树) ===")
        for tree in self.trees:
            tree.draw(canvas)
        print(f"=== 森林绘制完成, 共创建{TreeFactory.get_type_count()}种树木类型 ===\n")


if __name__ == "__main__":
    forest = Forest()

    trees_data = [
        (0, 0, "橡树", "绿色", "粗糙", "阔叶"),
        (1, 2, "橡树", "绿色", "粗糙", "阔叶"),
        (2, 4, "松树", "深绿", "光滑", "针叶"),
        (3, 1, "松树", "深绿", "光滑", "针叶"),
        (4, 3, "桦树", "白色", "光滑", "阔叶"),
    ]

    for x, y, name, color, texture, foliage in trees_data:
        forest.plant_tree(x, y, name, color, texture, foliage)

    forest.draw_all()
    print(f"实际树木数量: {len(forest.trees)}")
    print(f"唯一树木类型数量: {TreeFactory.get_type_count()}")
