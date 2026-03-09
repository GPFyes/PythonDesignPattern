"""
原型模式 - 入门级示例

简介：用最简单的方式演示原型模式的核心思想
"""

import copy


class Prototype:
    """原型基类"""
    def clone(self):
        return copy.deepcopy(self)


class Document(Prototype):
    """文档原型"""
    def __init__(self, title, content):
        self.title = title
        self.content = content
    
    def __str__(self):
        return f"Document(title={self.title}, content={self.content})"


if __name__ == "__main__":
    doc1 = Document("原始文档", "内容")
    doc2 = doc1.clone()
    doc2.title = "副本"
    print(doc1)
    print(doc2)
