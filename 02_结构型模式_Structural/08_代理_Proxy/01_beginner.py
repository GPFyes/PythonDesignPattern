"""代理模式 - 入门级示例"""

# 抽象主题类
class Subject:
    """定义真实主题和代理的公共接口"""
    def request(self):
        pass


# 真实主题类
class RealSubject(Subject):
    """真正执行业务逻辑的对象"""
    def request(self):
        return "真实对象的请求结果"


# 代理类
class Proxy(Subject):
    """持有真实主题的引用，控制对真实对象的访问"""
    def __init__(self):
        self.real_subject = RealSubject()
    
    def request(self):
        # 在访问真实对象前可以执行额外操作
        print("代理：访问前检查")
        result = self.real_subject.request()
        print("代理：访问后处理")
        return result


# 测试
if __name__ == "__main__":
    proxy = Proxy()
    result = proxy.request()
    print(result)
