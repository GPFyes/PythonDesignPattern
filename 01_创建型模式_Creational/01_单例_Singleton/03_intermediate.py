"""
单例模式 - 中级示例

简介：结合实际场景，展示配置管理器的应用
"""


class ConfigManager:
    """
    配置管理器 - 单例模式应用场景
    
    场景说明：
    在应用程序中，通常只需要一个配置管理器来管理全局配置信息。
    如果创建多个配置管理器实例，可能导致配置不一致的问题。
    """
    
    _instance = None  # 存储唯一实例
    
    def __new__(cls):
        """控制实例创建，确保只有一个实例"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """初始化配置"""
        # 避免重复初始化
        if self._initialized:
            return
        
        # 存储配置的字典
        self._config = {}
        self._initialized = True
    
    def set(self, key, value):
        """
        设置配置项
        
        Args:
            key: 配置键
            value: 配置值
        """
        self._config[key] = value
        print(f"[配置] 设置 {key} = {value}")
    
    def get(self, key, default=None):
        """
        获取配置项
        
        Args:
            key: 配置键
            default: 默认值（如果键不存在）
        
        Returns:
            配置值或默认值
        """
        return self._config.get(key, default)
    
    def get_all(self):
        """
        获取所有配置
        
        Returns:
            dict: 所有配置项的字典
        """
        return self._config.copy()


def main():
    """测试配置管理器"""
    print("=" * 50)
    print("测试单例模式 - 配置管理器")
    print("=" * 50)
    
    # 通过不同方式获取配置管理器
    config1 = ConfigManager()
    config2 = ConfigManager()
    
    # 验证是同一实例
    print(f"\n验证单例: config1 is config2 -> {config1 is config2}")
    
    # 设置配置（只有一份配置）
    print("\n--- 设置配置 ---")
    config1.set("app_name", "我的应用")
    config1.set("debug", True)
    config1.set("max_connections", 100)
    
    # 另一个引用也能看到配置
    print("\n--- 读取配置 ---")
    print(f"app_name: {config2.get('app_name')}")
    print(f"debug: {config2.get('debug')}")
    print(f"max_connections: {config2.get('max_connections')}")
    
    # 打印所有配置
    print(f"\n所有配置: {config1.get_all()}")
    
    print("\n" + "=" * 50)
    print("测试完成：所有引用共享同一份配置")
    print("=" * 50)


if __name__ == "__main__":
    main()
