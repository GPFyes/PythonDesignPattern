"""
工厂方法模式 - 简单级示例

简介：完整的工厂方法实现，展示动物工厂的例子
"""

from abc import ABC, abstractmethod


class Animal(ABC):
    """
    动物抽象类（产品角色）
    
    所有具体动物类都需要实现这个接口
    """
    
    @abstractmethod
    def speak(self):
        """动物发声"""
        pass


class Dog(Animal):
    """狗类（具体产品）"""
    
    def speak(self):
        return "汪汪！"


class Cat(Animal):
    """猫类（具体产品）"""
    
    def speak(self):
        return "喵喵！"


class AnimalFactory(ABC):
    """
    动物工厂抽象类（创建者角色）
    
    定义了创建动物的工厂方法
    """
    
    @abstractmethod
    def create_animal(self) -> Animal:
        """创建动物的工厂方法"""
        pass


class DogFactory(AnimalFactory):
    """狗工厂（具体创建者）"""
    
    def create_animal(self) -> Animal:
        return Dog()


class CatFactory(AnimalFactory):
    """猫工厂（具体创建者）"""
    
    def create_animal(self) -> Animal:
        return Cat()


def main():
    """测试工厂方法模式"""
    print("=" * 50)
    print("工厂方法模式 - 动物工厂")
    print("=" * 50)
    
    # 创建狗工厂并获取狗
    dog_factory = DogFactory()
    dog = dog_factory.create_animal()
    print(f"狗的发声: {dog.speak()}")
    
    # 创建猫工厂并获取猫
    cat_factory = CatFactory()
    cat = cat_factory.create_animal()
    print(f"猫的发声: {cat.speak()}")
    
    print("\n说明：")
    print("- DogFactory 创建 Dog 产品")
    print("- CatFactory 创建 Cat 产品")
    print("- 客户端只知道 Animal 接口，不知道具体类")


if __name__ == "__main__":
    main()
