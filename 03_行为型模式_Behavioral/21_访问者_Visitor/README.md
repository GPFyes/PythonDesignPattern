# 访问者模式 (Visitor)

> 表示一个作用于某对象结构中的各元素的操作。访问者使你可以在不改变各元素的类的前提下定义作用于这些元素的新操作。

## 模式结构

- **Visitor**: 抽象访问者，声明访问操作
- **ConcreteVisitor**: 具体访问者，实现每个由 Visitor 声明的操作
- **Element**: 抽象元素，接收访问者
- **ConcreteElement**: 具体元素，实现 accept 方法
- **ObjectStructure**: 对象结构，容纳多个元素

## 适用场景

- 对象结构中对象对应的类很少改变，但经常需要在此对象结构上定义新的操作
- 需要对一个对象结构中的对象进行很多不同的且不相关的操作
- 需要避免让这些操作"污染"这些对象的类

## 代码文件

| 文件 | 描述 |
|------|------|
| `beginner.py` | 入门级：最基本的访问者实现 |
| `simple.py` | 简单级：图形面积计算和绘制 |
| `intermediate.py` | 中级：文件系统操作 |
| `advanced.py` | 高级：完整 AST 解释器 |

## 学习要点

1. 理解双重分派机制
2. 掌握访问者模式的开闭原则
3. 注意访问者模式的适用场景

## 扩展阅读

- [Refactoring Guru - Visitor](https://refactoring.guru/design-patterns/visitor)
- [Visitor Pattern in Compiler Design](https://en.wikipedia.org/wiki/Visitor_pattern)
