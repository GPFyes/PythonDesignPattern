from abc import ABC, abstractmethod


class Command(ABC):
    @abstractmethod
    def execute(self):
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

    def get_status(self):
        return f"{self.location} 灯是{'开' if self.is_on else '关'}"


class LightOnCommand(Command):
    def __init__(self, light: Light):
        self.light = light

    def execute(self):
        self.light.on()


class LightOffCommand(Command):
    def __init__(self, light: Light):
        self.light = light

    def execute(self):
        self.light.off()


class RemoteControl:
    def __init__(self):
        self.slots = {}

    def set_command(self, slot: int, command: Command):
        self.slots[slot] = command

    def press_on(self, slot: int):
        if slot in self.slots:
            self.slots[slot].execute()
        else:
            print(f"插槽 {slot} 没有设置命令")

    def press_off(self, slot: int):
        if slot in self.slots:
            self.slots[slot].execute()
        else:
            print(f"插槽 {slot} 没有设置命令")


if __name__ == "__main__":
    living_room_light = Light("客厅")
    bedroom_light = Light("卧室")

    living_room_light_on = LightOnCommand(living_room_light)
    living_room_light_off = LightOffCommand(living_room_light)
    bedroom_light_on = LightOnCommand(bedroom_light)
    bedroom_light_off = LightOffCommand(bedroom_light)

    remote = RemoteControl()
    remote.set_command(0, living_room_light_on)
    remote.set_command(1, bedroom_light_on)

    print("=== 使用遥控器 ===")
    remote.press_on(0)
    remote.press_on(1)

    remote.set_command(0, living_room_light_off)
    remote.set_command(1, bedroom_light_off)

    print("\n=== 关闭灯 ===")
    remote.press_on(0)
    remote.press_on(1)

    print(f"\n{living_room_light.get_status()}")
    print(bedroom_light.get_status())
