"""
责任链模式 - 入门级示例
简单演示责任链模式的基本结构
"""


class Handler:
    """处理者抽象类"""
    
    def __init__(self):
        self.next_handler = None
    
    def set_next(self, handler):
        self.next_handler = handler
        return handler
    
    def handle(self, request):
        if self.next_handler:
            return self.next_handler.handle(request)
        return None


class ConcreteHandlerA(Handler):
    """具体处理者A"""
    
    def handle(self, request):
        if request == "A":
            return f"Handler A 处理了请求: {request}"
        return super().handle(request)


class ConcreteHandlerB(Handler):
    """具体处理者B"""
    
    def handle(self, request):
        if request == "B":
            return f"Handler B 处理了请求: {request}"
        return super().handle(request)


if __name__ == "__main__":
    handler_a = ConcreteHandlerA()
    handler_b = ConcreteHandlerB()
    
    handler_a.set_next(handler_b)
    
    print(handler_a.handle("A"))
    print(handler_a.handle("B"))
    print(handler_a.handle("C"))
