"""
中介者模式 - 入门级示例

简介：用最简单的方式演示中介者模式的核心思想
"""


class Mediator:
    def notify(self, sender, event: str) -> None:
        pass


class ChatRoom(Mediator):
    def __init__(self):
        self.users = []

    def notify(self, sender, event: str) -> None:
        for user in self.users:
            if user != sender:
                user.receive(event)


class User:
    def __init__(self, name: str, mediator: Mediator):
        self.name = name
        self.mediator = mediator

    def send(self, message: str) -> None:
        print(f"{self.name} 发送: {message}")
        self.mediator.notify(self, message)

    def receive(self, message: str) -> None:
        print(f"{self.name} 收到: {message}")


if __name__ == "__main__":
    chat_room = ChatRoom()

    alice = User("Alice", chat_room)
    bob = User("Bob", chat_room)
    charlie = User("Charlie", chat_room)

    chat_room.users.extend([alice, bob, charlie])

    alice.send("大家好！")
    print()
    bob.send("你好 Alice！")
    print()
    charlie.send("欢迎欢迎！")
