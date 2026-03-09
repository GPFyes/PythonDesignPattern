"""
建造者模式 - 高级示例

简介：生产级实现，展示完整的建造者模式
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List


class Product:
    """产品：复杂对象"""
    def __init__(self):
        self.parts: Dict[str, Any] = {}
    
    def add_part(self, name: str, part: Any):
        self.parts[name] = part
    
    def show(self):
        print("产品组成部分:")
        for name, part in self.parts.items():
            print(f"  {name}: {part}")


class Builder(ABC):
    """抽象建造者"""
    @abstractmethod
    def build_part_a(self):
        pass
    
    @abstractmethod
    def build_part_b(self):
        pass
    
    @abstractmethod
    def get_result(self) -> Product:
        pass


class ConcreteBuilder1(Builder):
    """具体建造者1"""
    def __init__(self):
        self.product = Product()
    
    def build_part_a(self):
        self.product.add_part("部件A1", "豪华部件A")
        return self
    
    def build_part_b(self):
        self.product.add_part("部件B1", "豪华部件B")
        return self
    
    def get_result(self) -> Product:
        return self.product


class ConcreteBuilder2(Builder):
    """具体建造者2"""
    def __init__(self):
        self.product = Product()
    
    def build_part_a(self):
        self.product.add_part("部件A2", "简约部件A")
        return self
    
    def build_part_b(self):
        self.product.add_part("部件B2", "简约部件B")
        return self
    
    def get_result(self) -> Product:
        return self.product


class Director:
    """指挥者"""
    def __init__(self, builder: Builder):
        self.builder = builder
    
    def construct(self):
        return self.builder.build_part_a().build_part_b().get_result()


if __name__ == "__main__":
    # 使用不同建造者
    director1 = Director(ConcreteBuilder1())
    product1 = director1.construct()
    product1.show()
    
    director2 = Director(ConcreteBuilder2())
    product2 = director2.construct()
    product2.show()
