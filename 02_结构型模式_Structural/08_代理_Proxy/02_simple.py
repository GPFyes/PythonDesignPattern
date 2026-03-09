"""代理模式 - 简单级示例"""


# 抽象主题接口
class IUserDao:
    """用户数据操作的抽象接口"""
    def get_user_id(self, user_id):
        pass

    def delete_user(self, user_id):
        pass


# 真实主题类 - 实际执行数据库操作
class UserDao(IUserDao):
    """真实的用户数据访问对象"""
    def __init__(self):
        print("连接数据库...")
    
    def get_user_id(self, user_id):
        print(f"从数据库查询用户ID: {user_id}")
        return {"id": user_id, "name": "张三"}
    
    def delete_user(self, user_id):
        print(f"从数据库删除用户: {user_id}")


# 代理类 - 控制对真实对象的访问
class UserDaoProxy(IUserDao):
    """用户数据操作的代理类"""
    def __init__(self):
        self.user_dao = None  # 懒加载
    
    def _get_real_subject(self):
        """延迟加载真实主题对象"""
        if self.user_dao is None:
            self.user_dao = UserDao()
        return self.user_dao
    
    def get_user_id(self, user_id):
        # 访问前验证
        if not isinstance(user_id, int) or user_id <= 0:
            print("代理：参数无效，拒绝访问")
            return None
        
        # 委托给真实对象
        result = self._get_real_subject().get_user_id(user_id)
        
        # 访问后记录日志
        print(f"代理：查询用户 {user_id} 的操作已记录")
        return result
    
    def delete_user(self, user_id):
        # 只有管理员才能删除用户
        print("代理：检查权限... 需要管理员权限")
        self._get_real_subject().delete_user(user_id)


# 测试
if __name__ == "__main__":
    proxy = UserDaoProxy()
    user = proxy.get_user_id(1)
    print(f"查询结果: {user}")
    print()
    proxy.delete_user(1)
