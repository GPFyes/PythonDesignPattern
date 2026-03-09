"""代理模式 - 中级示例：带权限控制的保护代理"""


from abc import ABC, abstractmethod
from datetime import datetime


class IFileService(ABC):
    """文件服务抽象接口"""
    @abstractmethod
    def read_file(self, filename):
        pass

    @abstractmethod
    def write_file(self, filename, content):
        pass

    @abstractmethod
    def delete_file(self, filename):
        pass


class RealFileService(IFileService):
    """真实的文件服务实现"""
    def __init__(self):
        self.storage = {}  # 模拟文件系统

    def read_file(self, filename):
        if filename in self.storage:
            return self.storage[filename]
        return None

    def write_file(self, filename, content):
        self.storage[filename] = content
        print(f"文件 '{filename}' 已写入")

    def delete_file(self, filename):
        if filename in self.storage:
            del self.storage[filename]
            print(f"文件 '{filename}' 已删除")
        else:
            print(f"文件 '{filename}' 不存在")


class User:
    """用户类"""
    def __init__(self, username, role):
        self.username = username
        self.role = role  # 'admin' 或 'user'


class ProtectedFileProxy(IFileService):
    """保护代理：控制不同用户对文件的访问权限"""
    def __init__(self, user):
        self.user = user
        self.real_service = None
        self.access_log = []

    def _check_permission(self, operation):
        """检查用户权限"""
        if operation == 'delete' and self.user.role != 'admin':
            print(f"权限拒绝：{self.user.username} 无权执行删除操作")
            return False
        if operation == 'write' and self.user.role == 'guest':
            print(f"权限拒绝：{self.user.username} 是访客，无权写入")
            return False
        return True

    def _get_real_service(self):
        if self.real_service is None:
            self.real_service = RealFileService()
        return self.real_service

    def _log_access(self, operation, filename, success):
        """记录访问日志"""
        log = {
            'user': self.user.username,
            'operation': operation,
            'filename': filename,
            'success': success,
            'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        self.access_log.append(log)

    def read_file(self, filename):
        if self._check_permission('read'):
            result = self._get_real_service().read_file(filename)
            self._log_access('read', filename, result is not None)
            return result
        return None

    def write_file(self, filename, content):
        if self._check_permission('write'):
            self._get_real_service().write_file(filename, content)
            self._log_access('write', filename, True)

    def delete_file(self, filename):
        if self._check_permission('delete'):
            self._get_real_service().delete_file(filename)
            self._log_access('delete', filename, True)

    def show_log(self):
        """查看访问日志"""
        print("\n=== 访问日志 ===")
        for log in self.access_log:
            status = "成功" if log['success'] else "失败"
            print(f"[{log['time']}] {log['user']} - {log['operation']} - {log['filename']} - {status}")


if __name__ == "__main__":
    admin = User("管理员", "admin")
    user = User("普通用户", "user")
    guest = User("访客", "guest")

    admin_proxy = ProtectedFileProxy(admin)
    user_proxy = ProtectedFileProxy(user)
    guest_proxy = ProtectedFileProxy(guest)

    # 管理员写入文件
    admin_proxy.write_file("secret.txt", "机密内容")

    # 普通用户尝试写入
    user_proxy.write_file("data.txt", "数据内容")

    # 访客尝试写入
    guest_proxy.write_file("guest.txt", "访客数据")

    # 管理员尝试删除
    admin_proxy.delete_file("secret.txt")

    # 普通用户尝试删除（应该失败）
    user_proxy.delete_file("data.txt")

    # 查看日志
    admin_proxy.show_log()
