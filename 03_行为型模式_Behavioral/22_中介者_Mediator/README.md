# 中介者模式 (Mediator)

> 用一个中介对象来封装一系列的对象交互。中介者使各对象不需要显式地相互引用，从而使其耦合松散。

## 模式结构

- **Mediator**: 中介者接口，定义对象间通信接口
- **ConcreteMediator**: 具体中介者，协调各同事对象
- **Colleague**: 同事类，各对象知道其中介者
- **ConcreteColleague**: 具体同事类

## 适用场景

- 系统中对象之间存在复杂的引用关系
- 想定制一个分布在多个类中的行为
- 想创建一个在所有对象之间使用的集中式控制面板

## 代码文件

| 文件 | 描述 |
|------|------|
| `beginner.py` | 入门级：最基本的聊天室中介者 |
| `simple.py` | 简单级：增加分组聊天室功能 |
| `intermediate.py` | 中级：UI 组件协调器 |
| `advanced.py` | 高级：完整的聊天系统 |

## 学习要点

1. 理解对象间耦合的复杂性
2. 掌握集中式控制的思想
3. 区分中介者模式和外观模式

## 扩展阅读

- [Refactoring Guru - Mediator](https://refactoring.guru/design-patterns/mediator)
- [MVC 框架中的中介者](https://en.wikipedia.org/wiki/Model%E2%80%93view%E2%80%93controller)
