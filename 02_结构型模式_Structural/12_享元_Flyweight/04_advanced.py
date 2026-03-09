from abc import ABC, abstractmethod
from typing import Dict, Tuple, Optional
import random


class Flyweight(ABC):
    @abstractmethod
    def operation(self, extrinsic_state: Dict) -> str:
        pass


class ConcreteFlyweight(Flyweight):
    def __init__(self, intrinsic_state: Tuple):
        self._intrinsic_state = intrinsic_state
        print(f"  [创建享元] 内部状态: {intrinsic_state}")

    def operation(self, extrinsic_state: Dict) -> str:
        return (f"享元操作 - 内部状态: {self._intrinsic_state}, "
                f"外部状态: {extrinsic_state}")


class UnsharedConcreteFlyweight(Flyweight):
    def __init__(self, state: Dict):
        self._state = state

    def operation(self, extrinsic_state: Dict) -> str:
        return f"非共享享元 - 全部状态: {self._state}, 外部: {extrinsic_state}"


class FlyweightFactory:
    _flyweights: Dict[str, ConcreteFlyweight] = {}

    @classmethod
    def get_flyweight(cls, key: str) -> ConcreteFlyweight:
        if key not in cls._flyweights:
            cls._flyweights[key] = ConcreteFlyweight(tuple(key.split("-")))
            print(f"[工厂] 创建新享元: {key}")
        else:
            print(f"[工厂] 复用已有享元: {key}")
        return cls._flyweights[key]

    @classmethod
    def get_count(cls) -> int:
        return len(cls._flyweights)

    @classmethod
    def list_flyweights(cls) -> None:
        print(f"\n=== 当前享元池 ({len(cls._flyweights)}个) ===")
        for key, fw in cls._flyweights.items():
            print(f"  {key}: {fw._intrinsic_state}")
        print()


class TreeTypeFlyweight:
    _types: Dict[Tuple, 'ConcreteTreeType'] = {}

    def __init__(self, name: str, color: str, texture: str):
        self.name = name
        self.color = color
        self.texture = texture
        self._render_data = self._load_render_data()

    def _load_render_data(self) -> Dict:
        return {"polygons": 1000, "textures": 1, "materials": 3}

    @classmethod
    def get_type(cls, name: str, color: str, texture: str) -> 'TreeTypeFlyweight':
        key = (name, color, texture)
        if key not in cls._types:
            cls._types[key] = TreeTypeFlyweight(name, color, texture)
            print(f"[树木工厂] 创建新树木类型: {name} ({color})")
        return cls._types[key]

    @classmethod
    def get_type_count(cls) -> int:
        return len(cls._types)


class Tree:
    def __init__(self, x: int, y: int, tree_type: TreeTypeFlyweight):
        self.x = x
        self.y = y
        self.tree_type = tree_type

    def draw(self) -> str:
        return f"在({self.x},{self.y})绘制{self.tree_type.color}{self.tree_type.name}"


class Forest:
    def __init__(self, name: str):
        self.name = name
        self.trees: list[Tree] = []

    def plant_tree(self, x: int, y: int, name: str, color: str, texture: str) -> None:
        tree_type = TreeTypeFlyweight.get_type(name, color, texture)
        tree = Tree(x, y, tree_type)
        self.trees.append(tree)

    def draw_all(self) -> None:
        print(f"\n{'='*50}")
        print(f"森林: {self.name}")
        print(f"树木总数: {len(self.trees)}")
        print(f"唯一类型数: {TreeTypeFlyweight.get_type_count()}")
        print(f"{'='*50}")
        for tree in self.trees:
            print(tree.draw())
        print()


class CharacterStyle:
    _styles: Dict[Tuple, 'CharacterStyle'] = {}

    def __init__(self, font: str, size: int, color: str):
        self.font = font
        self.size = size
        self.color = color

    @classmethod
    def get_style(cls, font: str, size: int, color: str) -> 'CharacterStyle':
        key = (font, size, color)
        if key not in cls._styles:
            cls._styles[key] = CharacterStyle(font, size, color)
        return cls._styles[key]

    @classmethod
    def get_count(cls) -> int:
        return len(cls._styles)


class Character:
    def __init__(self, char: str, x: int, y: int, style: CharacterStyle):
        self.char = char
        self.x = x
        self.y = y
        self.style = style


class Document:
    def __init__(self):
        self.characters: list[Character] = []

    def add_character(self, char: str, x: int, y: int, 
                      font: str, size: int, color: str) -> None:
        style = CharacterStyle.get_style(font, size, color)
        self.characters.append(Character(char, x, y, style))

    def render(self) -> None:
        print(f"\n文档渲染 ({len(self.characters)}个字符, "
              f"{CharacterStyle.get_count()}种样式)")
        for char in self.characters:
            print(f"  字符'{char.char}' at ({char.x},{char.y}) "
                  f"font={char.style.font}, size={char.style.size}")


def demo_basic_flyweight():
    print("\n" + "="*60)
    print("演示1: 基本享元模式")
    print("="*60)

    factory = FlyweightFactory()
    f1 = factory.get_flyweight("A-1-True")
    f2 = factory.get_flyweight("B-2-False")
    f3 = factory.get_flyweight("A-1-True")

    print(f1.operation({"user": "Alice"}))
    print(f2.operation({"user": "Bob"}))
    print(f3.operation({"user": "Charlie"}))

    print(f"\n享元总数: {factory.get_count()}")
    factory.list_flyweights()


def demo_forest():
    print("\n" + "="*60)
    print("演示2: 森林树木系统")
    print("="*60)

    forest = Forest("中央森林公园")
    trees_data = [
        (0, 0, "橡树", "绿色", "粗糙"),
        (1, 2, "橡树", "绿色", "粗糙"),
        (2, 4, "松树", "深绿", "光滑"),
        (3, 1, "松树", "深绿", "光滑"),
        (4, 3, "桦树", "白色", "光滑"),
        (5, 5, "橡树", "绿色", "粗糙"),
        (6, 2, "桦树", "白色", "光滑"),
    ]

    for x, y, name, color, texture in trees_data:
        forest.plant_tree(x, y, name, color, texture)

    forest.draw_all()


def demo_document():
    print("\n" + "="*60)
    print("演示3: 文档字符样式")
    print("="*60)

    doc = Document()
    text = "Hello World"
    x_start, y = 10, 20

    for i, char in enumerate(text):
        font = "Arial" if char.isupper() else "Times"
        size = 14 if char.isupper() else 12
        color = "黑色" if i % 2 == 0 else "蓝色"
        doc.add_character(char, x_start + i * 10, y, font, size, color)

    doc.render()


if __name__ == "__main__":
    demo_basic_flyweight()
    demo_forest()
    demo_document()
    print("\n演示完成!")
