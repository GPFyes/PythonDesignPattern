"""
适配器模式 - 入门级示例
"""

class Target:
    def request(self):
        return "Target: 默认行为"


class Adaptee:
    def specific_request(self):
        return ".eetpadA fo tsal fo siht"


class Adapter(Target):
    def __init__(self, adaptee):
        self.adaptee = adaptee
    
    def request(self):
        return self.adaptee.specific_request()[::-1]


if __name__ == "__main__":
    adapter = Adapter(Adaptee())
    print(adapter.request())
