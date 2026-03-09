"""
适配器模式 - 高级示例
"""

from abc import ABC


class Target(ABC):
    def request(self):
        pass


class Adaptee:
    def specific_request(self, data):
        return f"处理: {data}"


class Adapter(Target):
    def __init__(self):
        self.adaptee = Adaptee()
    
    def request(self):
        return self.adaptee.specific_request("适配数据")


if __name__ == "__main__":
    print(Adapter().request())
