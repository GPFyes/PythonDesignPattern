"""
中介者模式 - 简单级示例
"""

from abc import ABC, abstractmethod


class Mediator(ABC):
    @abstractmethod
    def notify(self, sender: "Colleague", event: str) -> None:
        pass


class Colleague(ABC):
    def __init__(self, mediator: Mediator):
        self.mediator = mediator


class ChatRoom(Mediator):
    def __init__(self):
        self.users = []

    def add_user(self, user: "User") -> None:
        self.users.append(user)

    def notify(self, sender: "Colleague", event: str) -> None:
        for user in self.users:
            if user != sender:
                user.receive(event)


class User(Colleague):
    def __init__(self, name: str, mediator: Mediator):
        super().__init__(mediator)
        self.name = name

    def send(self, message: str) -> None:
        print(f"{self.name} 发送: {message}")
        self.mediator.notify(self, message)

    def receive(self, message: str) -> None:
        print(f"{self.name} 收到: {message}")


class GroupChat(Mediator):
    def __init__(self):
        self.members = {}
        self.channels = {}

    def join(self, user: "GroupUser", channel: str) -> None:
        if channel not in self.channels:
            self.channels[channel] = []
        self.channels[channel].append(user)
        self.members[user.name] = channel
        print(f"{user.name} 加入频道: {channel}")

    def notify(self, sender: "Colleague", event: str) -> None:
        channel = self.members.get(sender.name)
        if channel and channel in self.channels:
            for member in self.channels[channel]:
                if member != sender:
                    member.receive(event)


class GroupUser(Colleague):
    def __init__(self, name: str, mediator: Mediator):
        super().__init__(mediator)
        self.name = name

    def send(self, message: str) -> None:
        print(f"[{self.name}] {message}")
        self.mediator.notify(self, message)

    def receive(self, message: str) -> None:
        print(f"  -> {self.name} 收到: {message}")


if __name__ == "__main__":
    print("=== 简单聊天室 ===")
    chat = ChatRoom()
    alice = User("Alice", chat)
    bob = User("Bob", chat)
    chat.add_user(alice)
    chat.add_user(bob)

    alice.send("你好！")
    print()
    bob.send("你好 Alice！")

    print("\n=== 分组聊天室 ===")
    group = GroupChat()
    user1 = GroupUser("张三", group)
    user2 = GroupUser("李四", group)
    user3 = GroupUser("王五", group)

    group.join(user1, "技术")
    group.join(user2, "技术")
    group.join(user3, "运营")

    user1.send("有人懂 Python 吗？")
    user3.send("我是做运营的")
