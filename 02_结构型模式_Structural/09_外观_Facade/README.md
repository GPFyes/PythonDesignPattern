# 外观模式（Facade Pattern）

## 定义
提供一个统一的高层次接口，使子系统更容易使用。

## 原理
封装复杂子系统，提供简单接口。外观类封装了子系统的复杂逻辑，对外提供简化的接口。

## 角色
- **Facade（外观）**：提供统一的高层次接口，封装子系统
- **Subsystem classes（子系统类）**：实现子系统功能，处理Facade委托的工作

## 优点
- 简化接口：客户端无需了解子系统内部复杂结构
- 解耦：客户端与子系统解耦，子系统修改不影响客户端

## 缺点
- 可能成为上帝类：外观类可能变得过于庞大和复杂
- 限制灵活性：客户端仍然可以直接访问子系统

## 适用场景
- 复杂子系统：需要简化对复杂子系统的访问
- 层次化系统：构建分层架构时，提供每层的入口
- 遗留系统：为复杂的遗留代码提供简化的接口

## 代码示例
- beginner.py：最基础的外观模式实现
- simple.py：简单外观示例
- intermediate.py：带多外观的示例
- advanced.py：完整的电脑启动/关闭系统示例

## 参考资料
- [外观模式 - 维基百科](https://en.wikipedia.org/wiki/Facade_pattern)
- [外观模式 - Refactoring Guru](https://refactoring.guru/design-patterns/facade)
