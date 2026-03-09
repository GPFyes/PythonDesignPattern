"""
工厂方法模式 - 入门级示例

简介：用最简单的方式演示工厂方法模式的核心思想
"""

from abc import ABC, abstractmethod


class Product(ABC):
    """产品抽象类"""
    
    @abstractmethod
    def operation(self):
        pass


class ConcreteProductA(Product):
    """具体产品A"""
    
    def operation(self):
        return "产品A的操作"


class ConcreteProductB(Product):
    """具体产品B"""
    
    def operation(self):
        return "产品B的操作"


class Creator(ABC):
    """创建者抽象类"""
    
    @abstractmethod
    def factory_method(self):
        pass


class ConcreteCreatorA(Creator):
    """创建者A：创建产品A"""
    
    def factory_method(self):
        return ConcreteProductA()


class ConcreteCreatorB(Creator):
    """创建者B：创建产品B"""
    
    def factory_method(self):
        return ConcreteProductB()


# 测试
if __name__ == "__main__":
    creator_a = ConcreteCreatorA()
    product_a = creator_a.factory_method()
    print(product_a.operation())
    
    creator_b = ConcreteCreatorB()
    product_b = creator_b.factory_method()
    print(product_b.operation())
