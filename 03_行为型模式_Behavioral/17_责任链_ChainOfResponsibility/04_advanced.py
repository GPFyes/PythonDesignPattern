"""
责任链模式 - 高级示例
演示支持异步处理和中间件系统的责任链实现
"""
import asyncio
from abc import ABC, abstractmethod
from typing import Any, Callable, Optional


class Middleware(ABC):
    """中间件抽象基类"""
    
    def __init__(self):
        self._next: Optional[Middleware] = None
    
    def use(self, middleware: 'Middleware') -> 'Middleware':
        self._next = middleware
        return middleware
    
    async def handle(self, context: dict) -> Any:
        processed = await self.process(context)
        if processed is not None:
            return processed
        if self._next:
            return await self._next.handle(context)
        return None
    
    @abstractmethod
    async def process(self, context: dict) -> Any:
        pass


class LoggingMiddleware(Middleware):
    """日志中间件"""
    
    async def process(self, context: dict) -> Any:
        print(f"[日志] 请求: {context.get('path', 'unknown')}")
        return None


class AuthMiddleware(Middleware):
    """认证中间件"""
    
    async def process(self, context: dict) -> Any:
        token = context.get("token")
        if not token or token != "valid_token":
            return {"error": "未授权", "status": 401}
        context["user"] = "authenticated_user"
        return None


class RateLimitMiddleware(Middleware):
    """限流中间件"""
    
    def __init__(self):
        super().__init__()
        self.requests = {}
    
    async def process(self, context: dict) -> Any:
        client_id = context.get("client_id", "default")
        import time
        current_time = int(time.time())
        
        if client_id not in self.requests:
            self.requests[client_id] = []
        
        self.requests[client_id] = [
            t for t in self.requests[client_id] 
            if current_time - t < 60
        ]
        
        if len(self.requests[client_id]) >= 10:
            return {"error": "请求过于频繁", "status": 429}
        
        self.requests[client_id].append(current_time)
        return None


class ValidationMiddleware(Middleware):
    """数据验证中间件"""
    
    async def process(self, context: dict) -> Any:
        required_fields = ["path", "method"]
        for field in required_fields:
            if field not in context:
                return {"error": f"缺少必要字段: {field}", "status": 400}
        
        if context.get("method") not in ["GET", "POST", "PUT", "DELETE"]:
            return {"error": "无效的HTTP方法", "status": 405}
        
        return None


class ResponseMiddleware(Middleware):
    """响应处理中间件"""
    
    async def process(self, context: dict) -> Any:
        return {
            "data": context.get("data", {}),
            "status": 200,
            "message": "成功"
        }


class MiddlewareChain:
    """中间件链管理器"""
    
    def __init__(self):
        self._middleware: Optional[Middleware] = None
    
    def add(self, middleware: Middleware) -> 'MiddlewareChain':
        if not self._middleware:
            self._middleware = middleware
        else:
            current = self._middleware
            while current._next:
                current = current._next
            current.use(middleware)
        return self
    
    async def execute(self, context: dict) -> Any:
        if self._middleware:
            return await self._middleware.handle(context)
        return None


class Router:
    """路由器"""
    
    def __init__(self):
        self._chains: dict[str, MiddlewareChain] = {}
    
    def register(self, path: str, chain: MiddlewareChain) -> None:
        self._chains[path] = chain
    
    async def handle_request(self, path: str, context: dict) -> Any:
        if path in self._chains:
            return await self._chains[path].execute(context)
        
        for pattern, chain in self._chains.items():
            if self._match_pattern(pattern, path):
                return await chain.execute(context)
        
        return {"error": "未找到路由", "status": 404}
    
    def _match_pattern(self, pattern: str, path: str) -> bool:
        if pattern.endswith("*"):
            return path.startswith(pattern[:-1])
        return pattern == path


async def main():
    router = Router()
    
    api_chain = (MiddlewareChain()
                 .add(LoggingMiddleware())
                 .add(AuthMiddleware())
                 .add(RateLimitMiddleware())
                 .add(ValidationMiddleware())
                 .add(ResponseMiddleware()))
    
    router.register("/api/*", api_chain)
    
    test_requests = [
        {"path": "/api/users", "method": "GET", "token": "valid_token", "client_id": "client1"},
        {"path": "/api/users", "method": "POST", "token": "invalid_token", "client_id": "client1"},
        {"path": "/api/data", "method": "GET", "token": "valid_token", "client_id": "client2"},
    ]
    
    for req in test_requests:
        print(f"\n处理请求: {req['path']} - {req['method']}")
        result = await router.handle_request(req["path"], req)
        print(f"结果: {result}")


if __name__ == "__main__":
    asyncio.run(main())
