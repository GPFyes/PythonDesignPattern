"""
抽象工厂模式 - 简单级示例

简介：完整的抽象工厂实现，展示 UI 组件工厂的例子
"""

from abc import ABC, abstractmethod


class Button(ABC):
    """按钮抽象类"""
    @abstractmethod
    def render(self):
        pass


class TextBox(ABC):
    """文本框抽象类"""
    @abstractmethod
    def render(self):
        pass


# Windows 风格组件
class WindowsButton(Button):
    def render(self):
        return "Windows 风格按钮"


class WindowsTextBox(TextBox):
    def render(self):
        return "Windows 风格文本框"


# Mac 风格组件
class MacButton(Button):
    def render(self):
        return "Mac 风格按钮"


class MacTextBox(TextBox):
    def render(self):
        return "Mac 风格文本框"


# 抽象工厂
class UIFactory(ABC):
    @abstractmethod
    def create_button(self):
        pass
    
    @abstractmethod
    def create_textbox(self):
        pass


# 具体工厂
class WindowsFactory(UIFactory):
    def create_button(self):
        return WindowsButton()
    
    def create_textbox(self):
        return WindowsTextBox()


class MacFactory(UIFactory):
    def create_button(self):
        return MacButton()
    
    def create_textbox(self):
        return MacTextBox()


def create_ui(factory: UIFactory):
    """使用工厂创建 UI 组件"""
    button = factory.create_button()
    textbox = factory.create_textbox()
    print(button.render())
    print(textbox.render())


if __name__ == "__main__":
    print("=== Windows UI ===")
    create_ui(WindowsFactory())
    print("\n=== Mac UI ===")
    create_ui(MacFactory())
