# 享元模式 (Flyweight Pattern)

## 定义
使用共享对象有效地支持大量细粒度对象。

## 原理
分离内部状态（可共享）和外部状态（不可共享），将内部状态存储在享元对象中，外部状态由客户端管理。

## 角色
- **Flyweight**: 抽象享元接口，定义操作
- **ConcreteFlyweight**: 具体享元实现，存储内部状态
- **FlyweightFactory**: 享元工厂，负责创建和管理享元对象
- **UnsharedConcreteFlyweight**: 不共享的具体享元

## 优点
- 节省内存空间
- 提高系统性能
- 减少对象数量

## 缺点
- 增加系统复杂度
- 需要分离内部/外部状态

## 适用场景
- 系统中存在大量相似对象
- 对象大部分状态可变为外部状态
- 多次重复创建相同对象

## 代码示例
- beginner.py - 入门示例
- simple.py - 简单示例
- intermediate.py - 中级示例
- advanced.py - 高级示例
