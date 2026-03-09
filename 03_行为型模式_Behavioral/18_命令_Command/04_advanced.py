from abc import ABC, abstractmethod
from datetime import datetime
from typing import List


class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def undo(self):
        pass


class Light:
    def __init__(self, location: str):
        self.location = location
        self.is_on = False
        self.brightness = 0

    def on(self, brightness=100):
        self.is_on = True
        self.brightness = brightness
        print(f"{self.location} 灯亮了 (亮度: {brightness}%)")

    def off(self):
        self.is_on = False
        self.brightness = 0
        print(f"{self.location} 灯关了")

    def dim(self, level: int):
        if self.is_on:
            self.brightness = max(0, min(100, level))
            print(f"{self.location} 灯亮度调整为 {self.brightness}%")


class LightOnCommand(Command):
    def __init__(self, light: Light, brightness: int = 100):
        self.light = light
        self.brightness = brightness
        self.previous_brightness = 0

    def execute(self):
        if not self.light.is_on:
            self.light.on(self.brightness)
        else:
            print(f"{self.light.location} 灯已经是开的")

    def undo(self):
        if self.previous_brightness > 0:
            self.light.on(self.previous_brightness)
        else:
            self.light.off()


class LightOffCommand(Command):
    def __init__(self, light: Light):
        self.light = light
        self.previous_brightness = 0

    def execute(self):
        if self.light.is_on:
            self.previous_brightness = self.light.brightness
            self.light.off()
        else:
            print(f"{self.light.location} 灯已经是关的")

    def undo(self):
        self.light.on(self.previous_brightness)


class MacroCommand(Command):
    def __init__(self, commands: List[Command]):
        self.commands = commands

    def execute(self):
        for command in self.commands:
            command.execute()

    def undo(self):
        for command in reversed(self.commands):
            command.undo()


class CommandHistory:
    def __init__(self):
        self.history: List[Command] = []
        self.redo_stack: List[Command] = []

    def execute(self, command: Command):
        command.execute()
        self.history.append(command)
        self.redo_stack.clear()

    def undo(self):
        if self.history:
            command = self.history.pop()
            command.undo()
            self.redo_stack.append(command)

    def redo(self):
        if self.redo_stack:
            command = self.redo_stack.pop()
            command.execute()
            self.history.append(command)

    def get_history(self):
        return self.history.copy()


class CommandLogger:
    def __init__(self):
        self.logs: List[dict] = []

    def log(self, action: str, command_name: str):
        entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "action": action,
            "command": command_name
        }
        self.logs.append(entry)
        print(f"[LOG] {entry['timestamp']} - {action}: {command_name}")

    def show_logs(self):
        print("\n=== 命令日志 ===")
        for log in self.logs:
            print(f"{log['timestamp']} - {log['action']}: {log['command']}")


class SmartRemoteControl:
    def __init__(self):
        self.slots: dict[int, Command] = {}
        self.history = CommandHistory()
        self.logger = CommandLogger()

    def set_command(self, slot: int, command: Command):
        self.slots[slot] = command

    def press_button(self, slot: int):
        if slot in self.slots:
            command = self.slots[slot]
            self.history.execute(command)
            self.logger.log("执行", command.__class__.__name__)
        else:
            print(f"插槽 {slot} 没有设置命令")

    def press_undo(self):
        if self.history.history:
            self.history.undo()
            self.logger.log("撤销", "UndoCommand")
        else:
            print("没有可撤销的命令")

    def press_redo(self):
        if self.history.redo_stack:
            self.history.redo()
            self.logger.log("重做", "RedoCommand")
        else:
            print("没有可重做的命令")

    def show_logs(self):
        self.logger.show_logs()


if __name__ == "__main__":
    living_room_light = Light("客厅")
    bedroom_light = Light("卧室")
    kitchen_light = Light("厨房")

    living_room_light_on = LightOnCommand(living_room_light)
    living_room_light_off = LightOffCommand(living_room_light)
    bedroom_light_on = LightOnCommand(bedroom_light)
    bedroom_light_off = LightOffCommand(bedroom_light)
    kitchen_light_on = LightOnCommand(kitchen_light)
    kitchen_light_off = LightOffCommand(kitchen_light)

    all_lights_on = MacroCommand([
        living_room_light_on,
        bedroom_light_on,
        kitchen_light_on
    ])

    all_lights_off = MacroCommand([
        living_room_light_off,
        bedroom_light_off,
        kitchen_light_off
    ])

    remote = SmartRemoteControl()

    remote.set_command(0, living_room_light_on)
    remote.set_command(1, living_room_light_off)
    remote.set_command(2, all_lights_on)
    remote.set_command(3, all_lights_off)

    print("=== 智能遥控器演示 ===\n")

    print("1. 打开客厅灯:")
    remote.press_button(0)

    print("\n2. 打开所有灯 (宏命令):")
    remote.press_button(2)

    print("\n3. 关闭所有灯 (宏命令):")
    remote.press_button(3)

    print("\n4. 撤销操作:")
    remote.press_undo()

    print("\n5. 再次撤销:")
    remote.press_undo()

    print("\n6. 重做操作:")
    remote.press_redo()

    print("\n7. 打开卧室灯:")
    remote.press_button(0)

    remote.show_logs()

    print("\n=== 当前灯状态 ===")
    print(f"客厅: {'开' if living_room_light.is_on else '关'}")
    print(f"卧室: {'开' if bedroom_light.is_on else '关'}")
    print(f"厨房: {'开' if kitchen_light.is_on else '关'}")
