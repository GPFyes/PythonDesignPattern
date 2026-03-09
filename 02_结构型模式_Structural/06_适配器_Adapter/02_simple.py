"""
适配器模式 - 简单级示例
"""

class Target:
    def request(self):
        return "默认行为"


class Adaptee:
    def specific_request(self):
        return "特殊请求"


class Adapter(Target):
    def __init__(self):
        self.adaptee = Adaptee()
    
    def request(self):
        return f"适配: {self.adaptee.specific_request()}"


if __name__ == "__main__":
    print(Adapter().request())
