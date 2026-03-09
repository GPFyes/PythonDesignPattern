"""
单例模式 - 高级示例

简介：生产级单例实现，包含线程安全、序列化支持、防止反射攻击
"""

import threading
import pickle
import json


class Singleton:
    """
    线程安全的单例模式实现
    
    特性：
    1. 线程安全：使用双重检查锁定（Double-Checked Locking）
    2. 防止反射攻击：__new__ 中检测实例是否已创建
    3. 序列化支持：__reduce__ 方法支持 pickle 序列化
    4. 防止多次实例化：类变量计数
    """
    
    _instance = None       # 存储唯一实例
    _lock = threading.Lock()  # 线程锁
    _created = False       # 标记是否已创建实例
    _instance_count = 0   # 实例计数
    
    def __new__(cls):
        """
        双重检查锁定的线程安全实现
        
        步骤：
        1. 第一次检查：避免不必要的锁竞争
        2. 加锁：确保线程安全
        3. 第二次检查：防止多个线程同时通过第一次检查
        """
        # 第一次检查：实例已存在则直接返回
        if cls._instance is not None:
            return cls._instance
        
        # 加锁：确保线程安全
        with cls._lock:
            # 第二次检查：双重检查锁定
            if cls._instance is None:
                # 创建实例
                instance = super().__new__(cls)
                # 初始化实例属性
                instance._created = True
                cls._instance = instance
                cls._instance_count += 1
        
        return cls._instance
    
    def __init__(self):
        """初始化方法，防止重复初始化"""
        # 防止反射攻击：已创建过的实例不再重新初始化
        if not self._created:
            self._created = True
    
    def __reduce__(self):
        """
        支持 pickle 序列化
        
        当对象被序列化时，直接返回已有实例而不是创建新实例
        """
        return (self.__class__, ())
    
    def __repr__(self):
        """返回对象的字符串表示"""
        return f"<{self.__class__.__name__} object at {hex(id(self))}>"
    
    @classmethod
    def get_instance(cls):
        """
        静态方法获取实例
        
        Returns:
            Singleton: 唯一实例
        """
        if cls._instance is None:
            cls()
        return cls._instance
    
    @classmethod
    def reset_instance(cls):
        """
        重置实例（仅用于测试）
        
        Warning: 此方法会破坏单例模式，请谨慎使用
        """
        with cls._lock:
            cls._instance = None
            cls._created = False
            cls._instance_count = 0
    
    @classmethod
    def get_instance_count(cls):
        """
        获取实例数量
        
        Returns:
            int: 实例数量
        """
        return cls._instance_count


class DatabaseConnection:
    """
    数据库连接单例 - 生产环境示例
    
    场景：数据库连接池通常只需要一个实例
    """
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls, *args, **kwargs):
        """线程安全的单例实现"""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._connected = False
        return cls._instance
    
    def __init__(self, host="localhost", port=3306):
        """初始化数据库连接"""
        if not hasattr(self, '_initialized') or not self._initialized:
            self.host = host
            self.port = port
            self._initialized = True
            self._connected = False
    
    def connect(self):
        """建立数据库连接"""
        if not self._connected:
            print(f"连接数据库: {self.host}:{self.port}")
            self._connected = True
            return True
        print("已连接到数据库")
        return False
    
    def disconnect(self):
        """断开数据库连接"""
        if self._connected:
            print("断开数据库连接")
            self._connected = False
    
    def query(self, sql):
        """执行查询"""
        if not self._connected:
            print("请先连接数据库")
            return None
        print(f"执行查询: {sql}")
        return []


def test_thread_safety():
    """测试线程安全性"""
    print("\n" + "=" * 50)
    print("测试线程安全性")
    print("=" * 50)
    
    results = []
    
    def create_instance():
        """线程函数：创建实例"""
        instance = Singleton()
        results.append(id(instance))
    
    # 创建多个线程同时创建实例
    threads = [threading.Thread(target=create_instance) for _ in range(10)]
    
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    
    # 验证所有线程获取的是同一实例
    unique_ids = set(results)
    print(f"创建的实例数量: {len(unique_ids)}")
    print(f"线程安全: {len(unique_ids) == 1}")


def test_database_connection():
    """测试数据库连接单例"""
    print("\n" + "=" * 50)
    print("测试数据库连接单例")
    print("=" * 50)
    
    # 获取多个连接引用
    conn1 = DatabaseConnection(host="192.168.1.100", port=3306)
    conn2 = DatabaseConnection(host="192.168.1.200", port=3307)
    
    # 验证是同一实例（忽略初始化参数）
    print(f"conn1 is conn2: {conn1 is conn2}")
    
    # 连接和查询
    conn1.connect()
    conn2.query("SELECT * FROM users")
    
    # 关闭连接（影响所有引用）
    conn1.disconnect()


def test_serialization():
    """测试序列化支持"""
    print("\n" + "=" * 50)
    print("测试序列化支持")
    print("=" * 50)
    
    # 创建实例
    original = Singleton()
    original_id = id(original)
    print(f"原始实例 ID: {original_id}")
    
    # 序列化
    serialized = pickle.dumps(original)
    print(f"序列化成功，长度: {len(serialized)} 字节")
    
    # 反序列化
    deserialized = pickle.loads(serialized)
    deserialized_id = id(deserialized)
    print(f"反序列化实例 ID: {deserialized_id}")
    
    # 验证是同一实例
    print(f"反序列化后是同一实例: {original_id == deserialized_id}")


def main():
    """主函数"""
    print("=" * 50)
    print("单例模式 - 生产级实现测试")
    print("=" * 50)
    
    # 测试基本功能
    print("\n--- 基本功能测试 ---")
    s1 = Singleton()
    s2 = Singleton()
    print(f"s1 is s2: {s1 is s2}")
    print(f"实例数量: {Singleton.get_instance_count()}")
    
    # 测试线程安全
    test_thread_safety()
    
    # 测试数据库连接
    test_database_connection()
    
    # 测试序列化
    test_serialization()
    
    print("\n" + "=" * 50)
    print("所有测试完成")
    print("=" * 50)


if __name__ == "__main__":
    main()
