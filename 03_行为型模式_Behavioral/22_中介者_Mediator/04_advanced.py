"""
中介者模式 - 高级示例

实现一个完整的聊天系统，支持私聊、群聊、房间管理
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Set
from datetime import datetime
import threading


class Message:
    def __init__(self, sender: str, content: str, msg_type: str = "text"):
        self.sender = sender
        self.content = content
        self.msg_type = msg_type
        self.timestamp = datetime.now()


class Mediator(ABC):
    @abstractmethod
    def broadcast(self, sender: str, message: Message) -> None:
        pass

    @abstractmethod
    def send_to(self, sender: str, receiver: str, message: Message) -> None:
        pass

    @abstractmethod
    def join(self, user: "User") -> None:
        pass

    @abstractmethod
    def leave(self, user: str) -> None:
        pass


class ChatRoom(Mediator):
    def __init__(self, name: str):
        self.name = name
        self.users: Dict[str, "User"] = {}
        self.history: List[Message] = []
        self.lock = threading.Lock()
        self.admins: Set[str] = set()

    def broadcast(self, sender: str, message: Message) -> None:
        with self.lock:
            self.history.append(message)
            for user in self.users.values():
                if user.name != sender:
                    user.receive(message)

    def send_to(self, sender: str, receiver: str, message: Message) -> None:
        with self.lock:
            if receiver in self.users:
                self.history.append(message)
                self.users[receiver].receive(message)
            else:
                raise ValueError(f"用户不存在: {receiver}")

    def join(self, user: "User") -> None:
        with self.lock:
            self.users[user.name] = user
            join_msg = Message("系统", f"{user.name} 加入了聊天室")
            self.history.append(join_msg)
            self.broadcast("系统", join_msg)

    def leave(self, user: str) -> None:
        with self.lock:
            if user in self.users:
                del self.users[user]
                leave_msg = Message("系统", f"{user} 离开了聊天室")
                self.history.append(leave_msg)
                self.broadcast("System", leave_msg)

    def get_users(self) -> List[str]:
        return list(self.users.keys())

    def get_history(self, limit: int = 10) -> List[Message]:
        return self.history[-limit:]


class PrivateChat(Mediator):
    def __init__(self):
        self.chats: Dict[str, Dict[str, "User"]] = {}
        self.lock = threading.Lock()

    def start_chat(self, user1: "User", user2: "User") -> None:
        with self.lock:
            key = f"{min(user1.name, user2.name)}_{max(user1.name, user2.name)}"
            self.chats[key] = {user1.name: user1, user2.name: user2}

    def broadcast(self, sender: str, message: Message) -> None:
        pass

    def send_to(self, sender: str, receiver: str, message: Message) -> None:
        with self.lock:
            for chat in self.chats.values():
                if sender in chat and receiver in chat:
                    chat[receiver].receive(message)
                    return
            raise ValueError(f"未找到与 {receiver} 的私聊")

    def join(self, user: "User") -> None:
        pass

    def leave(self, user: str) -> None:
        pass


class User:
    def __init__(self, name: str, mediator: Mediator):
        self.name = name
        self.mediator = mediator
        self.unread: List[Message] = []
        self.status = "online"

    def send(self, content: str) -> None:
        message = Message(self.name, content)
        self.mediator.broadcast(self.name, message)

    def send_to(self, receiver: str, content: str) -> None:
        message = Message(self.name, content)
        self.mediator.send_to(self.name, receiver, message)

    def receive(self, message: Message) -> None:
        self.unread.append(message)
        time_str = message.timestamp.strftime("%H:%M")
        print(f"[{time_str}] {message.sender} -> {self.name}: {message.content}")

    def get_unread(self) -> List[Message]:
        messages = self.unread.copy()
        self.unread.clear()
        return messages

    def join_room(self) -> None:
        self.mediator.join(self)
        self.status = "online"

    def leave_room(self) -> None:
        self.mediator.leave(self.name)
        self.status = "offline"


class ChatSystem:
    def __init__(self):
        self.rooms: Dict[str, ChatRoom] = {}
        self.private_chat = PrivateChat()
        self.users: Dict[str, User] = {}
        self.default_room: Optional[ChatRoom] = None

    def create_room(self, name: str) -> ChatRoom:
        room = ChatRoom(name)
        self.rooms[name] = room
        return room

    def add_user(self, name: str, room: Optional[ChatRoom] = None) -> User:
        user = User(name, room or self.default_room)
        self.users[name] = user
        if room:
            user.join_room()
        return user

    def set_default_room(self, room: ChatRoom) -> None:
        self.default_room = room


def demo_basic_chat():
    print("=== 基本聊天功能 ===")
    room = ChatRoom("Python学习群")

    alice = User("Alice", room)
    bob = User("Bob", room)
    charlie = User("Charlie", room)

    room.join(alice)
    room.join(bob)
    room.join(charlie)

    print()
    alice.send("大家好！")
    print()
    bob.send("你好 Alice！")
    print()
    charlie.send("欢迎欢迎！")


def demo_private_chat():
    print("\n=== 私聊功能 ===")
    room = ChatRoom("技术交流群")

    alice = User("Alice", room)
    bob = User("Bob", room)

    room.join(alice)
    room.join(bob)

    alice.send_to("Bob", "悄悄话：今晚一起吃饭？")


def demo_chat_history():
    print("\n=== 聊天记录 ===")
    room = ChatRoom("测试房间")

    user1 = User("用户1", room)
    user2 = User("用户2", room)

    room.join(user1)
    room.join(user2)

    user1.send("第一条消息")
    user2.send("第二条消息")
    user1.send("第三条消息")

    print("\n最近聊天记录:")
    for msg in room.get_history(5):
        time_str = msg.timestamp.strftime("%H:%M:%S")
        print(f"  [{time_str}] {msg.sender}: {msg.content}")


def demo_multi_room():
    print("\n=== 多房间系统 ===")
    system = ChatSystem()

    room1 = system.create_room("Python")
    room2 = system.create_room("Java")
    room3 = system.create_room("Go")

    alice = system.add_user("Alice", room1)
    bob = system.add_user("Bob", room2)
    charlie = system.add_user("Charlie", room3)

    print(f"Python房间用户: {room1.get_users()}")
    print(f"Java房间用户: {room2.get_users()}")
    print(f"Go房间用户: {room3.get_users()}")


if __name__ == "__main__":
    demo_basic_chat()
    demo_private_chat()
    demo_chat_history()
    demo_multi_room()
