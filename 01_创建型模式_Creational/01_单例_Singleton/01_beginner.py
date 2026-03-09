"""
单例模式 - 入门级示例

简介：用最简单的方式演示单例模式的核心思想
"""

class Singleton:
    """单例类：通过重写 __new__ 方法控制实例创建"""
    _instance = None  # 类变量，存储唯一实例
    
    def __new__(cls):
        """创建或返回唯一实例"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

# 测试
if __name__ == "__main__":
    a = Singleton()
    b = Singleton()
    print(f"a is b: {a is b}")  # True，说明是同一实例
