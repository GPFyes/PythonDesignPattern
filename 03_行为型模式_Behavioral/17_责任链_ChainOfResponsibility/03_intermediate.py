"""
责任链模式 - 中级示例
演示用户认证系统的责任链实现
"""


class AuthHandler:
    """认证处理器基类"""
    
    def __init__(self):
        self.next_handler = None
    
    def set_next(self, handler):
        self.next_handler = handler
        return handler
    
    def authenticate(self, user):
        if self.next_handler:
            return self.next_handler.authenticate(user)
        return True


class UsernameHandler(AuthHandler):
    """用户名验证处理器"""
    
    def authenticate(self, user):
        if not user.get("username"):
            print("错误: 用户名不能为空")
            return False
        print(f"用户名验证通过: {user['username']}")
        return super().authenticate(user)


class PasswordHandler(AuthHandler):
    """密码验证处理器"""
    
    def authenticate(self, user):
        if not user.get("password"):
            print("错误: 密码不能为空")
            return False
        if len(user["password"]) < 6:
            print("错误: 密码长度必须至少为6位")
            return False
        print("密码验证通过")
        return super().authenticate(user)


class EmailHandler(AuthHandler):
    """邮箱验证处理器"""
    
    def authenticate(self, user):
        email = user.get("email", "")
        if not email or "@" not in email:
            print("错误: 无效的邮箱地址")
            return False
        print(f"邮箱验证通过: {email}")
        return super().authenticate(user)


class AgeHandler(AuthHandler):
    """年龄验证处理器"""
    
    def authenticate(self, user):
        age = user.get("age", 0)
        if age < 18:
            print("错误: 用户必须年满18岁")
            return False
        print(f"年龄验证通过: {age}岁")
        return super().authenticate(user)


if __name__ == "__main__":
    username_handler = UsernameHandler()
    password_handler = PasswordHandler()
    email_handler = EmailHandler()
    age_handler = AgeHandler()
    
    username_handler.set_next(password_handler).set_next(email_handler).set_next(age_handler)
    
    test_users = [
        {"username": "john", "password": "123456", "email": "john@example.com", "age": 25},
        {"username": "jane", "password": "123", "email": "jane@example.com", "age": 20},
        {"username": "bob", "password": "123456", "email": "bob@example.com", "age": 16},
    ]
    
    for user in test_users:
        print(f"\n测试用户: {user['username']}")
        result = username_handler.authenticate(user)
        print(f"认证结果: {'通过' if result else '失败'}")
