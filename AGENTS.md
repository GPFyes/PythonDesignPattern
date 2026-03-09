# AGENTS.md - Agent 编码指南

本文件为 Python 设计模式学习仓库的 AI Agent 提供编码指南。

## 项目概述

这是一个 Python 设计模式教育仓库，实现 GoF 23 种设计模式。每种模式有四个难度级别：入门级（~15行）、简单级（~30行）、中级（~60行）、高级（~100行）。

## 仓库结构

```
├── 01_创建型模式_Creational/    # 创建型模式 (5种)
│   ├── 01_单例_Singleton/
│   ├── 02_工厂方法_FactoryMethod/
│   ├── 03_抽象工厂_AbstractFactory/
│   ├── 04_建造者_Builder/
│   └── 05_原型_Prototype/
├── 02_结构型模式_Structural/   # 结构型模式 (7种)
│   ├── 06_适配器_Adapter/
│   ├── 07_装饰器_Decorator/
│   ├── 08_代理_Proxy/
│   ├── 09_外观_Facade/
│   ├── 10_桥接_Bridge/
│   ├── 11_组合_Composite/
│   └── 12_享元_Flyweight/
├── 03_行为型模式_Behavioral/   # 行为型模式 (11种)
│   ├── 13_策略_Strategy/
│   ├── 14_模板方法_TemplateMethod/
│   ├── 15_观察者_Observer/
│   ├── 16_迭代器_Iterator/
│   ├── 17_责任链_ChainOfResponsibility/
│   ├── 18_命令_Command/
│   ├── 19_备忘录_Memento/
│   ├── 20_状态_State/
│   ├── 21_访问者_Visitor/
│   ├── 22_中介者_Mediator/
│   └── 23_解释器_Interpreter/
├── pyproject.toml
└── README.md
```

每种模式目录包含：`beginner.py`、`simple.py`、`intermediate.py`、`advanced.py`、`README.md`

## 构建/测试命令

### 运行 Python 文件

```bash
# 直接运行
python behavioral/command/beginner.py
python creational/singleton/advanced.py

# 使用模块方式
python -m behavioral.command.beginner
```

### 测试

**注意**：本仓库无正式单元测试。每个 `*.py` 文件包含 `main()` 函数或测试函数，可直接执行。

```bash
# 运行文件
python creational/singleton/advanced.py

# 运行特定测试函数
python -c "from creational.singleton.advanced import test_thread_safety; test_thread_safety()"
```

### 无正式 Lint/Format 配置

如需添加工具，推荐：ruff、black、mypy、pytest

```toml
# pyproject.toml 示例
[tool.ruff]
line-length = 100

[tool.ruff.lint]
select = ["E", "F", "I", "N", "W"]
ignore = ["E501"]
```

## 代码风格指南

### 格式规范

- **缩进**：4空格
- **行长度**：软限制100字符
- **空行**：顶级定义间两行，方法间一行
- **无尾随空格**

### 导入顺序

```python
# 标准库
import threading
import json

# 第三方库
from abc import ABC, abstractmethod
from typing import List, Optional
```

### 命名规范

| 类型 | 规范 | 示例 |
|------|------|------|
| 类 | PascalCase | `class Singleton:` |
| 函数 | snake_case | `def get_instance():` |
| 变量 | snake_case | `instance = None` |
| 常量 | UPPER_SNAKE | `MAX_CONNECTIONS = 10` |

### 类型注解

```python
def create_instance(name: str) -> Optional[object]:
    pass
```

### 错误处理

教育代码保持简单：
```python
if instance is None:
    raise ValueError("Instance cannot be None")
```

### 文件结构模板

```python
"""
{Pattern Name} - {Difficulty Level}
描述...
"""

from abc import ABC, abstractmethod
from typing import Optional


class ExampleClass:
    """简短描述"""
    
    def __init__(self, param: str):
        self.param = param
    
    def method(self) -> None:
        """方法描述"""
        pass


def main():
    """主入口"""
    pass


if __name__ == "__main__":
    main()
```

### 语言规范

- 使用中文注释
- README.md 使用中文

## 常见任务

### 添加新模式

1. 创建目录：`behavioral/new-pattern/`
2. 创建文件：4个难度级别文件
3. 更新主 README.md
4. 创建模式 README.md

## Agent 注意事项

- 这是教育仓库 - 清晰优先于技巧
- 每个文件应自包含（无跨文件依赖）
- 高级文件需包含：线程安全（如适用）、错误处理、边缘情况、文档
- 无需添加复杂构建基础设施
