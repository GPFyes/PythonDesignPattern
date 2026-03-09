# 解释器模式 (Interpreter)

> 给定一个语言，定义它的文法表示，并定义一个解释器，这个解释器使用该表示来解释语言中的句子。

## 模式结构

- **AbstractExpression**: 抽象解释器，声明解释操作
- **TerminalExpression**: 终结符表达式，实现与文法中的终结符相关的解释操作
- **NonterminalExpression**: 非终结符表达式，文法中的每条规则对应一个非终结符表达式
- **Context**: 包含解释器之外的一些全局信息
- **Client**: 构建抽象语法树，调用解释操作

## 适用场景

- 重复发生的问题可以用一种简单的语言来表达
- 简单语法，需要解释一些特定句子
- 不太复杂的语法场景

## 代码文件

| 文件 | 描述 |
|------|------|
| `beginner.py` | 入门级：最基本的解释器实现 |
| `simple.py` | 简单级：增加 AND、OR 操作符 |
| `intermediate.py` | 中级：实现变量环境和更复杂的表达式 |
| `advanced.py` | 高级：完整的数学表达式解析器 |

## 学习要点

1. 理解抽象语法树（AST）的构建
2. 掌握递归下降解析的基本原理
3. 了解解释器模式的优缺点

## 扩展阅读

- [Refactoring Guru - Interpreter](https://refactoring.guru/design-patterns/interpreter)
- [Python AST 模块](https://docs.python.org/3/library/ast.html)
