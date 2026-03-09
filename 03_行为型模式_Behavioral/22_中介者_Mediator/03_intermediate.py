"""
中介者模式 - 中级示例

实现一个简单的 UI 组件协调器
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional


class Mediator(ABC):
    @abstractmethod
    def notify(self, sender: "Component", event: str) -> None:
        pass


class Component(ABC):
    def __init__(self, mediator: Optional[Mediator] = None):
        self.mediator = mediator

    def set_mediator(self, mediator: Mediator) -> None:
        self.mediator = mediator


class Button(Component):
    def __init__(self, label: str, mediator: Optional[Mediator] = None):
        super().__init__(mediator)
        self.label = label
        self.enabled = True
        self.clicked_handlers: List[callable] = []

    def click(self) -> None:
        if self.enabled:
            print(f"按钮 [{self.label}] 被点击")
            for handler in self.clicked_handlers:
                handler()
            if self.mediator:
                self.mediator.notify(self, "click")

    def set_enabled(self, enabled: bool) -> None:
        self.enabled = enabled
        state = "启用" if enabled else "禁用"
        print(f"按钮 [{self.label}] 已{state}")

    def on_click(self, handler: callable) -> None:
        self.clicked_handlers.append(handler)


class TextBox(Component):
    def __init__(self, name: str, mediator: Optional[Mediator] = None):
        super().__init__(mediator)
        self.name = name
        self.text = ""
        self.readonly = False

    def set_text(self, text: str) -> None:
        if not self.readonly:
            self.text = text
            print(f"文本框 [{self.name}] 内容: {text}")
            if self.mediator:
                self.mediator.notify(self, "text_changed")

    def get_text(self) -> str:
        return self.text

    def clear(self) -> None:
        self.text = ""
        print(f"文本框 [{self.name}] 已清空")
        if self.mediator:
            self.mediator.notify(self, "text_cleared")


class Label(Component):
    def __init__(self, text: str, mediator: Optional[Mediator] = None):
        super().__init__(mediator)
        self.text = text

    def set_text(self, text: str) -> None:
        self.text = text
        print(f"标签: {text}")

    def get_text(self) -> str:
        return self.text


class FormDialog(Mediator):
    def __init__(self):
        self.username_input: Optional[TextBox] = None
        self.password_input: Optional[TextBox] = None
        self.submit_button: Optional[Button] = None
        self.status_label: Optional[Label] = None

    def set_components(
        self, username: TextBox, password: TextBox, button: Button, label: Label
    ) -> None:
        self.username_input = username
        self.password_input = password
        self.submit_button = button
        self.status_label = label

        username.set_mediator(self)
        password.set_mediator(self)
        button.set_mediator(self)
        label.set_mediator(self)

    def notify(self, sender: Component, event: str) -> None:
        if event == "text_changed":
            self._validate_form()
        elif event == "click":
            self._submit_form()
        elif event == "text_cleared":
            self._validate_form()

    def _validate_form(self) -> None:
        username = self.username_input.get_text() if self.username_input else ""
        password = self.password_input.get_text() if self.password_input else ""

        is_valid = len(username) >= 3 and len(password) >= 6

        if self.submit_button:
            self.submit_button.set_enabled(is_valid)

        if self.status_label:
            if not username and not password:
                self.status_label.set_text("请输入用户名和密码")
            elif len(username) < 3:
                self.status_label.set_text("用户名至少3个字符")
            elif len(password) < 6:
                self.status_label.set_text("密码至少6个字符")
            else:
                self.status_label.set_text("表单有效")

    def _submit_form(self) -> None:
        username = self.username_input.get_text() if self.username_input else ""
        password = self.password_input.get_text() if self.password_input else ""
        print(f"\n提交表单: 用户名={username}, 密码={'*' * len(password)}")


if __name__ == "__main__":
    print("=== UI 表单对话框 ===\n")

    form = FormDialog()

    username_box = TextBox("username")
    password_box = TextBox("password")
    submit_btn = Button("提交")
    status_lbl = Label("请输入用户名和密码")

    form.set_components(username_box, password_box, submit_btn, status_lbl)

    print("1. 输入用户名 'ab':")
    username_box.set_text("ab")
    print()

    print("2. 输入密码 '12345' (太短):")
    password_box.set_text("12345")
    print()

    print("3. 输入密码 '123456':")
    password_box.set_text("123456")
    print()

    print("4. 用户名补全 'abc':")
    username_box.set_text("abc")
    print()

    print("5. 点击提交按钮:")
    submit_btn.click()
