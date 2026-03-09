"""
原型模式 - 简单级示例

简介：展示完整的原型模式实现
"""

import copy
from abc import ABC


class Prototype(ABC):
    """抽象原型类"""
    def clone(self):
        return copy.deepcopy(self)


class User(Prototype):
    """用户原型"""
    def __init__(self, name, email, roles=None):
        self.name = name
        self.email = email
        self.roles = roles or []
    
    def __str__(self):
        return f"User(name={self.name}, email={self.email}, roles={self.roles})"


if __name__ == "__main__":
    user1 = User("张三", "zhangsan@example.com", ["admin", "user"])
    user2 = user1.clone()
    user2.name = "李四"
    print(user1)
    print(user2)
