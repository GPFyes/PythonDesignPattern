"""
原型模式 - 高级示例

简介：展示完整的原型模式实现，包含深浅拷贝
"""

import copy
from typing import Dict, Any


class Prototype:
    """抽象原型类"""
    def clone(self):
        return copy.deepcopy(self)


class Address:
    """地址类"""
    def __init__(self, city, street):
        self.city = city
        self.street = street
    
    def __str__(self):
        return f"{self.city}, {self.street}"


class Person(Prototype):
    """人物类"""
    def __init__(self, name, age, address: Address):
        self.name = name
        self.age = age
        self.address = address
    
    def __str__(self):
        return f"{self.name}, {self.age}岁, 住在{self.address}"
    
    def shallow_clone(self):
        """浅拷贝"""
        return copy.copy(self)
    
    def deep_clone(self):
        """深拷贝"""
        return copy.deepcopy(self)


if __name__ == "__main__":
    addr = Address("北京", "朝阳区")
    person1 = Person("张三", 30, addr)
    
    # 深拷贝
    person2 = person1.deep_clone()
    person2.name = "李四"
    person2.address.city = "上海"
    
    print("原对象:", person1)
    print("深拷贝:", person2)
