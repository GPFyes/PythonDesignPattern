# Python 设计模式学习


## 快速导航

| 模式类型 | 难度 | 推荐学习顺序 |
|----------|------|--------------|
| 创建型 | ⭐⭐ | 1-2-3-4-5 |
| 结构型 | ⭐⭐⭐ | 1-2-3-4-5-6-7 |
| 行为型 | ⭐⭐⭐⭐ | 1-2-3-4-5-6-7-8-9-10-11 |

需要知道的基础：
- [设计模式背景](#设计模式背景)
- [设计模式核心思想](#设计模式核心思想)
- [设计模式原则（SOLID）](#设计模式原则solid)
- [接口与设计模式](#接口与设计模式的关系)


## 目录

### 创建型模式（5种）
创建型模式专注于对象创建机制。

1. [01_单例_Singleton](./01_创建型模式_Creational/01_单例_Singleton/README.md) - 保证类只有一个实例
2. [02_工厂方法_FactoryMethod](./01_创建型模式_Creational/02_工厂方法_FactoryMethod/README.md) - 由子类决定实例化哪个类
3. [03_抽象工厂_AbstractFactory](./01_创建型模式_Creational/03_抽象工厂_AbstractFactory/README.md) - 创建一系列相关对象
4. [04_建造者_Builder](./01_创建型模式_Creational/04_建造者_Builder/README.md) - 分离复杂对象构建与表示
5. [05_原型_Prototype](./01_创建型模式_Creational/05_原型_Prototype/README.md) - 通过复制原型创建新对象

### 结构型模式（7种）
结构型模式关注对象组合。

6. [06_适配器_Adapter](./02_结构型模式_Structural/06_适配器_Adapter/README.md) - 接口转换
7. [07_装饰器_Decorator](./02_结构型模式_Structural/07_装饰器_Decorator/README.md) - 动态添加职责
8. [08_代理_Proxy](./02_结构型模式_Structural/08_代理_Proxy/README.md) - 控制对象访问
9. [09_外观_Facade](./02_结构型模式_Structural/09_外观_Facade/README.md) - 简化复杂子系统
10. [10_桥接_Bridge](./02_结构型模式_Structural/10_桥接_Bridge/README.md) - 分离抽象与实现
11. [11_组合_Composite](./02_结构型模式_Structural/11_组合_Composite/README.md) - 树形结构
12. [12_享元_Flyweight](./02_结构型模式_Structural/12_享元_Flyweight/README.md) - 共享对象

### 行为型模式（11种）
行为型模式关注对象交互。

13. [13_策略_Strategy](./03_行为型模式_Behavioral/13_策略_Strategy/README.md) - 算法封装
14. [14_模板方法_TemplateMethod](./03_行为型模式_Behavioral/14_模板方法_TemplateMethod/README.md) - 算法骨架
15. [15_观察者_Observer](./03_行为型模式_Behavioral/15_观察者_Observer/README.md) - 一对多依赖
16. [16_迭代器_Iterator](./03_行为型模式_Behavioral/16_迭代器_Iterator/README.md) - 统一遍历
17. [17_责任链_ChainOfResponsibility](./03_行为型模式_Behavioral/17_责任链_ChainOfResponsibility/README.md) - 请求传递
18. [18_命令_Command](./03_行为型模式_Behavioral/18_命令_Command/README.md) - 请求封装
19. [19_备忘录_Memento](./03_行为型模式_Behavioral/19_备忘录_Memento/README.md) - 状态保存
20. [20_状态_State](./03_行为型模式_Behavioral/20_状态_State/README.md) - 状态影响行为
21. [21_访问者_Visitor](./03_行为型模式_Behavioral/21_访问者_Visitor/README.md) - 操作分离
22. [22_中介者_Mediator](./03_行为型模式_Behavioral/22_中介者_Mediator/README.md) - 集中交互
23. [23_解释器_Interpreter](./03_行为型模式_Behavioral/23_解释器_Interpreter/README.md) - 语言解析

---
## 设计模式背景
**GoF**（Gang of Four，四人帮）是指 Erich Gamma、Richard Helm、Ralph Johnson 和 John Vlissides 四位软件工程专家。他们于1994年出版了《Design Patterns: Elements of Reusable Object-Oriented Software》一书，首次系统性地总结了23种面向对象设计模式。

---

## 设计模式核心思想

- **封装变化**：找出程序中变化的部分，将其与不变的部分分离
- **面向接口编程**：针对抽象类型编程，而不是针对具体实现
- **组合优于继承**：优先使用对象组合来实现复用

---

## 设计模式原则

### 一、SOLID 原则

#### 1. S —— 单一职责原则
-   **核心思想：** 一个类只负责一个职责。
-   **通俗理解：** 不该管的别管，避免成为什么都做的“上帝类”。
-   **优点：** 降低类复杂度，提高可读性和可维护性。

#### 2. O —— 开闭原则
-   **核心思想：** 对扩展开放，对修改关闭。
-   **通俗理解：** 加新功能时写新代码，尽量不动旧代码。
-   **优点：** 提高系统稳定性和可维护性，降低修改旧代码的风险。

#### 3. L —— 里氏替换原则
-   **核心思想：** 子类必须能完全替换父类，且程序逻辑不变。
-   **通俗理解：** 凡是用父类的地方，换成子类也得跑得通。
-   **优点：** 约束继承滥用，确保多态的正确性。

#### 4. I —— 接口隔离原则
-   **核心思想：** 客户端不应依赖它不需要的接口。
-   **通俗理解：** 接口要小而精，不要大而全，避免实现类包含空方法。
-   **优点：** 降低代码耦合度，提高系统灵活性。

#### 5. D —— 依赖倒置原则
-   **核心思想：** 面向接口编程，依赖抽象而非具体实现。
-   **通俗理解：** 电脑主板依赖标准的插槽接口，而不依赖具体的硬件品牌。
-   **优点：** 极大降低类间耦合，便于替换和维护。

---

### 二、其他重要设计原则

#### 6. 迪米特法则 （最少知识原则）
-   **核心思想：** 一个对象应对其他对象有最少的了解。
-   **通俗理解：** 只与直接的朋友（自身、成员、参数、内部创建对象）通信，不和“陌生人”说话。
-   **优点：** 降低类间耦合，提高系统可读性和稳定性。
-   **潜在缺点：** 可能需要创建大量中介类，增加系统复杂度。

#### 7. 合成复用原则 （组合/聚合复用原则）
-   **核心思想：** 尽量使用对象组合（has-a）而不是继承（is-a）来达到复用目的。
-   **通俗理解：** 如果你需要一辆车，组合的思路是“我有一辆车”（买零件组装），而不是“我是一辆车”（自己造所有零件）。
-   **优点：** 降低耦合度，提高灵活性（可在运行时动态替换），不破坏封装。
-   **风险提示：** 继承容易导致基类脆弱问题（父类修改影响所有子类）。


---

## 设计模式与原则的关系

| 设计原则 | 相关设计模式 |
|----------|-------------|
| 单一职责 | 策略模式、命令模式、装饰器模式 |
| 开闭原则 | 策略模式、装饰器模式、访问者模式 |
| 里氏替换 | 策略模式、模板方法模式、状态模式 |
| 接口隔离 | 装饰器模式、代理模式、迭代器模式 |
| 依赖倒置 | 工厂方法模式、抽象工厂模式、依赖注入 |
| 迪米特法则 | 中介者模式、外观模式 |
| 合成复用 | 组合模式、装饰器模式、代理模式 |

---

## 接口与设计模式

### 接口在设计模式中的作用

接口是设计模式的核心组成部分，主要作用包括：

1. **定义抽象层**：通过接口定义行为规范，将"做什么"与"怎么做"分离
2. **解耦实现**：客户端依赖接口而非具体实现，便于替换和扩展
3. **实现多态**：同一接口可以有多种实现，运行时动态选择
4. **约束行为**：确保实现类提供特定的方法和能力

### 接口与设计模式的关系

| 接口类型 | 相关设计模式 | 说明 |
|---------|-------------|------|
| **产品接口** | 工厂方法、抽象工厂 | 定义产品对象的统一接口 |
| **策略接口** | 策略模式、状态模式 | 封装可互换的算法 |
| **迭代器接口** | 迭代器模式 | 统一遍历不同集合的方式 |
| **命令接口** | 命令模式 | 封装请求为对象 |
| **观察者接口** | 观察者模式 | 定义通知机制 |
| **组件接口** | 组合模式、装饰器模式 | 统一组件行为 |
| **访问者接口** | 访问者模式 | 定义对元素的操作 |
| **中介者接口** | 中介者模式 | 定义对象间通信 |
| **适配器接口** | 适配器模式 | 统一不同接口 |
| **代理接口** | 代理模式 | 控制对对象的访问 |

### Python 中接口的实现方式

Python 使用多种方式实现接口概念：

#### 1. 抽象基类（ABC）

```python
from abc import ABC, abstractmethod

class Drawable(ABC):
    @abstractmethod
    def draw(self):
        pass

class Circle(Drawable):
    def draw(self):
        print("绘制圆形")

class Rectangle(Drawable):
    def draw(self):
        print("绘制矩形")
```

#### 2. Protocol（结构子类型）

```python
from typing import Protocol

class Drawable(Protocol):
    def draw(self) -> None:
        ...

# 无需显式继承，结构兼容即可
class Circle:
    def draw(self):
        print("绘制圆形")
```

#### 3. Duck Typing

```python
# 只需对象具有 draw 方法即可
def draw_shape(shape):
    shape.draw()  # 不需要显式接口声明
```

### 设计模式中接口的使用示例

```python
# 策略模式：策略接口
class PaymentStrategy(ABC):
    @abstractmethod
    def pay(self, amount):
        pass

# 状态模式：状态接口
class State(ABC):
    @abstractmethod
    def handle(self, context):
        pass

# 命令模式：命令接口
class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

# 观察者模式：观察者接口
class Observer(ABC):
    @abstractmethod
    def update(self, data):
        pass

# 迭代器模式：迭代器接口
class Iterator(ABC):
    @abstractmethod
    def __next__(self):
        pass
    
    @abstractmethod
    def __iter__(self):
        pass
```

### 接口设计的最佳实践

1. **保持接口小而专注**：遵循接口隔离原则
2. **使用抽象类而非具体类**：依赖抽象而非具体
3. **避免肥接口**：将大接口拆分为小接口
4. **为接口命名要描述行为**：使用动词或形容词
5. **考虑未来扩展**：接口应具有通用性

---

## 学习建议

### 每种模式学习步骤
1. **阅读笔记** - 理解概念和原理
2. **入门级代码** - 掌握核心思想
3. **简单级代码** - 理解完整结构
4. **中级代码** - 了解实际应用
5. **高级代码** - 生产级实现

### 代码示例说明
每个模式目录下包含 4 个代码文件：
- `01_beginner.py` - 入门级（约15行）
- `02_simple.py` - 简单级（约30行）
- `03_intermediate.py` - 中级（约60行）
- `04_advanced.py` - 高级（约100行）

---

