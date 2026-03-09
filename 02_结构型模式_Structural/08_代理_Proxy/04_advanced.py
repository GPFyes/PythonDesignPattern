"""代理模式 - 高级示例：综合多种代理类型的完整系统"""


from abc import ABC, abstractmethod
from datetime import datetime
import time
import os


class IImage(ABC):
    """图像抽象接口"""
    @abstractmethod
    def display(self):
        pass

    @abstractmethod
    def get_info(self):
        pass


class RealImage(IImage):
    """真实图像类 - 模拟加载大型图像文件"""
    def __init__(self, filename):
        self.filename = filename
        self.load_from_disk()

    def load_from_disk(self):
        """模拟从磁盘加载大型图像的耗时操作"""
        print(f"[加载] 正在从磁盘加载图像: {self.filename}")
        time.sleep(1)  # 模拟耗时操作
        self.data = f"图像数据: {self.filename}"
        self.resolution = "1920x1080"
        self.size = os.path.getsize(__file__) if os.path.exists(__file__) else 1024

    def display(self):
        print(f"[显示] 正在显示图像: {self.filename}")

    def get_info(self):
        return {
            'filename': self.filename,
            'resolution': self.resolution,
            'size': self.size,
            'data': self.data
        }


class VirtualProxyImage(IImage):
    """虚代理 - 延迟加载大型图像"""
    def __init__(self, filename):
        self.filename = filename
        self.real_image = None

    def _load_if_needed(self):
        if self.real_image is None:
            self.real_image = RealImage(self.filename)

    def display(self):
        self._load_if_needed()
        self.real_image.display()

    def get_info(self):
        self._load_if_needed()
        return self.real_image.get_info()


class ImageProxyWithCache(IImage):
    """带缓存的代理 - 缓存图像信息，避免重复加载"""
    def __init__(self, filename):
        self.filename = filename
        self.real_image = None
        self.cache_info = None
        self.load_count = 0

    def _load_if_needed(self):
        if self.real_image is None:
            self.real_image = RealImage(self.filename)
            self.load_count += 1

    def display(self):
        self._load_if_needed()
        print(f"[缓存代理] 显示图像 (加载次数: {self.load_count})")
        self.real_image.display()

    def get_info(self):
        if self.cache_info is None:
            self._load_if_needed()
            self.cache_info = self.real_image.get_info()
            print(f"[缓存代理] 首次获取信息，已缓存")
        else:
            print(f"[缓存代理] 从缓存获取信息")
        return self.cache_info


class LoggingProxyImage(IImage):
    """日志代理 - 记录图像操作日志"""
    def __init__(self, image):
        self.image = image
        self.access_log = []

    def _log(self, action):
        log_entry = {
            'action': action,
            'filename': self.image.filename if hasattr(self.image, 'filename') else 'unknown',
            'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        self.access_log.append(log_entry)
        print(f"[日志] {action} - {log_entry['time']}")

    def display(self):
        self._log("display")
        self.image.display()

    def get_info(self):
        self._log("get_info")
        return self.image.get_info()

    def show_logs(self):
        print("\n=== 访问日志 ===")
        for log in self.access_log:
            print(f"  {log['time']} - {log['action']} - {log['filename']}")


class AccessControlProxy(IImage):
    """访问控制代理 - 控制对图像的访问权限"""
    def __init__(self, image, user_role):
        self.image = image
        self.user_role = user_role

    def _check_permission(self):
        if self.user_role not in ['admin', 'vip', 'user']:
            print(f"[访问控制] 拒绝 {self.user_role} 访问图像")
            return False
        return True

    def display(self):
        if self._check_permission():
            self.image.display()
        else:
            print("[访问控制] 显示默认占位图像")

    def get_info(self):
        if self._check_permission():
            return self.image.get_info()
        return {'error': '权限不足', 'role': self.user_role}


class ImageFactory:
    """图像工厂 - 根据配置创建不同类型的代理"""
    @staticmethod
    def create_image(filename, use_proxy=True, enable_logging=False, role='user'):
        image = VirtualProxyImage(filename)
        
        if enable_logging:
            image = LoggingProxyImage(image)
        
        image = AccessControlProxy(image, role)
        
        return image


def demonstrate_proxy_pattern():
    """演示代理模式"""
    print("=" * 60)
    print("代理模式演示")
    print("=" * 60)

    print("\n--- 1. 虚代理：延迟加载 ---")
    print("创建代理时不会立即加载图像")
    virtual_proxy = VirtualProxyImage("photo.jpg")
    print("代理已创建，图像尚未加载")
    
    print("\n首次访问时才加载：")
    virtual_proxy.display()
    
    print("\n再次访问（使用缓存）：")
    virtual_proxy.display()

    print("\n--- 2. 带缓存的代理 ---")
    cache_proxy = ImageProxyWithCache("landscape.png")
    print("获取图像信息（首次）：")
    info1 = cache_proxy.get_info()
    
    print("\n再次获取信息（从缓存）：")
    info2 = cache_proxy.get_info()

    print("\n--- 3. 日志代理 ---")
    real_image = RealImage("test.jpg")
    logged_image = LoggingProxyImage(real_image)
    logged_image.display()
    logged_image.get_info()
    logged_image.show_logs()

    print("\n--- 4. 访问控制代理 ---")
    admin_image = AccessControlProxy(RealImage("admin_only.jpg"), 'admin')
    guest_image = AccessControlProxy(RealImage("admin_only.jpg"), 'guest')
    
    print("\n管理员访问：")
    admin_image.display()
    
    print("\n访客访问：")
    guest_image.display()

    print("\n--- 5. 组合多种代理 ---")
    print("使用工厂创建组合代理：")
    combined = ImageFactory.create_image(
        filename="composed.jpg", 
        enable_logging=True, 
        role='vip'
    )
    combined.display()
    combined.get_info()


if __name__ == "__main__":
    demonstrate_proxy_pattern()
