"""
单例模式 - 简单级示例

简介：完整的单例实现，包含基础注释说明
"""


class Singleton:
    """
    单例模式实现类
    
    通过类变量 _instance 保存唯一实例，
    在 __new__ 方法中判断实例是否已存在，
    如果存在则返回已有实例，否则创建新实例
    """
    
    _instance = None  # 类变量，保存唯一实例
    
    def __new__(cls):
        """
        重写 __new__ 方法控制实例创建
        
        Returns:
            Singleton: 唯一实例
        """
        # 如果实例不存在，则创建新实例
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        # 返回已有实例
        return cls._instance
    
    def __init__(self):
        """初始化方法，用于设置实例属性"""
        # 可以在这里添加初始化逻辑
        pass


def main():
    """测试单例模式"""
    # 创建两个实例
    instance1 = Singleton()
    instance2 = Singleton()
    
    # 验证是同一实例
    print(f"instance1 is instance2: {instance1 is instance2}")
    print(f"id(instance1): {id(instance1)}")
    print(f"id(instance2): {id(instance2)}")


if __name__ == "__main__":
    main()
