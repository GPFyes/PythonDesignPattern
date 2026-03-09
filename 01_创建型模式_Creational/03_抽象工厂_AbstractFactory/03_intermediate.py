"""
抽象工厂模式 - 中级示例

简介：结合实际场景，展示跨平台 UI 组件的应用
"""

from abc import ABC, abstractmethod
from typing import List


class Button(ABC):
    """按钮抽象类"""
    @abstractmethod
    def render(self):
        pass
    
    @abstractmethod
    def on_click(self, callback):
        pass


class TextBox(ABC):
    """文本框抽象类"""
    @abstractmethod
    def render(self):
        pass
    
    @abstractmethod
    def get_text(self):
        pass


class CheckBox(ABC):
    """复选框抽象类"""
    @abstractmethod
    def render(self):
        pass
    
    @abstractmethod
    def is_checked(self):
        pass


# Windows 风格组件
class WindowsButton(Button):
    def __init__(self, text):
        self.text = text
        self.callback = None
    
    def render(self):
        return f"[Windows Button: {self.text}]"
    
    def on_click(self, callback):
        self.callback = callback
        return f"Windows 按钮绑定点击事件"


class WindowsTextBox(TextBox):
    def __init__(self):
        self.text = ""
    
    def render(self):
        return f"[Windows TextBox: {self.text or 'empty'}]"
    
    def get_text(self):
        return self.text


class WindowsCheckBox(CheckBox):
    def __init__(self):
        self.checked = False
    
    def render(self):
        state = "✓" if self.checked else "□"
        return f"[Windows CheckBox: {state}]"
    
    def is_checked(self):
        return self.checked


# Mac 风格组件
class MacButton(Button):
    def __init__(self, text):
        self.text = text
        self.callback = None
    
    def render(self):
        return f"<Mac Button: {self.text}>"
    
    def on_click(self, callback):
        self.callback = callback
        return "Mac 按钮绑定点击事件"


class MacTextBox(TextBox):
    def __init__(self):
        self.text = ""
    
    def render(self):
        return f"<Mac TextBox: {self.text or 'empty'}>"
    
    def get_text(self):
        return self.text


class MacCheckBox(CheckBox):
    def __init__(self):
        self.checked = False
    
    def render(self):
        state = "☑" if self.checked else "☐"
        return f"<Mac CheckBox: {state}>"
    
    def is_checked(self):
        return self.checked


# 抽象工厂
class UIFactory(ABC):
    @abstractmethod
    def create_button(self, text: str):
        pass
    
    @abstractmethod
    def create_textbox(self):
        pass
    
    @abstractmethod
    def create_checkbox(self):
        pass


# 具体工厂
class WindowsFactory(UIFactory):
    def create_button(self, text: str):
        return WindowsButton(text)
    
    def create_textbox(self):
        return WindowsTextBox()
    
    def create_checkbox(self):
        return WindowsCheckBox()


class MacFactory(UIFactory):
    def create_button(self, text: str):
        return MacButton(text)
    
    def create_textbox(self):
        return MacTextBox()
    
    def create_checkbox(self):
        return MacCheckBox()


class UIPage:
    """UI 页面，使用工厂创建组件"""
    
    def __init__(self, factory: UIFactory):
        self.factory = factory
        self.components = []
    
    def create_login_form(self):
        """创建登录表单"""
        title = self.factory.create_button("登录")
        username = self.factory.create_textbox()
        remember = self.factory.create_checkbox()
        
        self.components = [title, username, remember]
        return self.components
    
    def render(self):
        """渲染所有组件"""
        print("\n" + "=" * 50)
        print("登录页面")
        print("=" * 50)
        for comp in self.components:
            print(comp.render())


def main():
    """测试抽象工厂模式"""
    print("=" * 50)
    print("抽象工厂模式 - 跨平台 UI 组件")
    print("=" * 50)
    
    # Windows 风格
    windows_page = UIPage(WindowsFactory())
    windows_page.create_login_form()
    windows_page.render()
    
    # Mac 风格
    mac_page = UIPage(MacFactory())
    mac_page.create_login_form()
    mac_page.render()
    
    print("\n说明：")
    print("- 切换工厂即可切换整个产品族")
    print("- 确保同一产品族内的组件风格一致")


if __name__ == "__main__":
    main()
