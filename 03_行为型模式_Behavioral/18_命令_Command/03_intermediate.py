from abc import ABC, abstractmethod


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

    def on(self):
        self.is_on = True
        print(f"{self.location} 灯亮了")

    def off(self):
        self.is_on = False
        print(f"{self.location} 灯关了")


class LightOnCommand(Command):
    def __init__(self, light: Light):
        self.light = light

    def execute(self):
        if not self.light.is_on:
            self.light.on()
        else:
            print(f"{self.light.location} 灯已经是开的")

    def undo(self):
        self.light.off()


class LightOffCommand(Command):
    def __init__(self, light: Light):
        self.light = light

    def execute(self):
        if self.light.is_on:
            self.light.off()
        else:
            print(f"{self.light.location} 灯已经是关的")

    def undo(self):
        self.light.on()


class RemoteControlWithUndo:
    def __init__(self):
        self.history = []
        self.undo_stack = []

    def execute_command(self, command: Command):
        command.execute()
        self.history.append(command)
        self.undo_stack.clear()

    def undo(self):
        if self.history:
            command = self.history.pop()
            print(f"撤销: ", end="")
            command.undo()
            self.undo_stack.append(command)
        else:
            print("没有可撤销的命令")

    def redo(self):
        if self.undo_stack:
            command = self.undo_stack.pop()
            print(f"重做: ", end="")
            command.execute()
            self.history.append(command)
        else:
            print("没有可重做的命令")


if __name__ == "__main__":
    living_room_light = Light("客厅")

    light_on = LightOnCommand(living_room_light)
    light_off = LightOffCommand(living_room_light)

    remote = RemoteControlWithUndo()

    print("=== 执行命令 ===")
    remote.execute_command(light_on)
    remote.execute_command(light_off)
    remote.execute_command(light_on)

    print("\n=== 撤销操作 ===")
    remote.undo()
    remote.undo()

    print("\n=== 重做操作 ===")
    remote.redo()
    remote.redo()

    print("\n=== 再撤销 ===")
    remote.undo()
