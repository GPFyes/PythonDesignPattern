"""
抽象工厂模式 - 入门级示例

简介：用最简单的方式演示抽象工厂模式的核心思想
"""

from abc import ABC, abstractmethod


# 抽象产品 A
class ProductA(ABC):
    @abstractmethod
    def operation_a(self):
        pass


# 抽象产品 B
class ProductB(ABC):
    @abstractmethod
    def operation_b(self):
        pass


# 具体产品 A1, A2
class ConcreteProductA1(ProductA):
    def operation_a(self):
        return "产品A1"


class ConcreteProductA2(ProductA):
    def operation_a(self):
        return "产品A2"


# 具体产品 B1, B2
class ConcreteProductB1(ProductB):
    def operation_b(self):
        return "产品B1"


class ConcreteProductB2(ProductB):
    def operation_b(self):
        return "产品B2"


# 抽象工厂
class AbstractFactory(ABC):
    @abstractmethod
    def create_product_a(self):
        pass
    
    @abstractmethod
    def create_product_b(self):
        pass


# 具体工厂1：生产产品族1
class ConcreteFactory1(AbstractFactory):
    def create_product_a(self):
        return ConcreteProductA1()
    
    def create_product_b(self):
        return ConcreteProductB1()


# 具体工厂2：生产产品族2
class ConcreteFactory2(AbstractFactory):
    def create_product_a(self):
        return ConcreteProductA2()
    
    def create_product_b(self):
        return ConcreteProductB2()


# 测试
if __name__ == "__main__":
    factory1 = ConcreteFactory1()
    print(factory1.create_product_a().operation_a())
    print(factory1.create_product_b().operation_b())
    
    factory2 = ConcreteFactory2()
    print(factory2.create_product_a().operation_a())
    print(factory2.create_product_b().operation_b())
