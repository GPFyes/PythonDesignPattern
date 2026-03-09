# 桥接模式 (Bridge Pattern)

## 定义
将抽象部分与实现部分分离，使它们可以独立变化。

## 原理
通过组合代替继承。桥接模式的核心是将抽象部分和实现部分分别抽象出来，通过组合关系将两者连接起来，从而实现解耦。

## 角色
- **Abstraction（抽象部分）**：定义抽象类的接口，维护一个指向 Implementor 的引用
- **RefinedAbstraction（扩展抽象类）**：扩展 Abstraction 的接口
- **Implementor（实现部分）**：定义实现类的接口
- **ConcreteImplementor（具体实现类）**：实现 Implementor 接口的具体类

## 优点
1. 分离抽象与实现，使得两者可以独立变化
2. 扩展性强，可以独立扩展抽象部分和实现部分
3. 符合开闭原则
4. 客户端代码只需要与高层抽象交互，降低耦合

## 缺点
1. 增加系统复杂度
2. 需要正确识别系统中两个独立变化的维度

## 适用场景
1. 不想绑定抽象和实现，希望两者可以独立扩展
2. 类的抽象和实现都需要通过子类来特化
3. 希望避免继承带来的静态绑定
4. 图形绘制系统（如形状与渲染器的组合）

## 代码示例
- beginner.py: 入门示例
- simple.py: 简单示例
- intermediate.py: 中级示例
- advanced.py: 高级示例

## 经典示例：形状(Shape)和渲染器(Renderer)
形状（Circle、Square 等）与渲染方式（VectorRenderer、RasterRenderer）的组合是桥接模式的经典应用。
