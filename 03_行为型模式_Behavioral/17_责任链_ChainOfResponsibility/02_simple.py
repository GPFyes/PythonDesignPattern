"""
责任链模式 - 简单级示例
演示日志系统的责任链实现
"""


class LogHandler:
    """日志处理器基类"""
    
    def __init__(self, level):
        self.level = level
        self.next_handler = None
    
    def set_next(self, handler):
        self.next_handler = handler
        return handler
    
    def handle(self, message, level):
        if level >= self.level:
            self.write(message)
        if self.next_handler:
            self.next_handler.handle(message, level)
    
    def write(self, message):
        raise NotImplementedError


class DebugHandler(LogHandler):
    """调试日志处理器"""
    
    def __init__(self):
        super().__init__(1)
    
    def write(self, message):
        print(f"[DEBUG] {message}")


class InfoHandler(LogHandler):
    """信息日志处理器"""
    
    def __init__(self):
        super().__init__(2)
    
    def write(self, message):
        print(f"[INFO] {message}")


class ErrorHandler(LogHandler):
    """错误日志处理器"""
    
    def __init__(self):
        super().__init__(3)
    
    def write(self, message):
        print(f"[ERROR] {message}")


if __name__ == "__main__":
    debug = DebugHandler()
    info = InfoHandler()
    error = ErrorHandler()
    
    debug.set_next(info).set_next(error)
    
    print("发送调试级别日志:")
    debug.handle("这是一个调试信息", 1)
    
    print("\n发送信息级别日志:")
    debug.handle("这是一个信息", 2)
    
    print("\n发送错误级别日志:")
    debug.handle("这是一个错误", 3)
