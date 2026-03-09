"""外观模式 - 中级示例"""


class CPU:
    def __init__(self):
        self.is_running = False

    def freeze(self):
        print("CPU: 冻结处理器状态")
        self.is_running = False

    def jump(self, position):
        print(f"CPU: 跳转到位置 {position}")

    def execute(self):
        print("CPU: 执行指令")
        self.is_running = True


class Memory:
    def __init__(self):
        self.data = {}

    def load(self, position, data):
        print(f"Memory: 加载数据到位置 {position}")
        self.data[position] = data

    def clear(self):
        print("Memory: 清除内存")
        self.data.clear()


class Disk:
    def read_boot_sector(self):
        print("Disk: 读取启动扇区")
        return "boot_data"


class ComputerFacade:
    def __init__(self):
        self.cpu = CPU()
        self.memory = Memory()
        self.disk = Disk()

    def start(self):
        print("=" * 30)
        print("启动电脑...")
        boot_data = self.disk.read_boot_sector()
        self.memory.load(0, boot_data)
        self.cpu.jump(0)
        self.cpu.execute()
        print("=" * 30)

    def shutdown(self):
        print("=" * 30)
        print("关闭电脑...")
        self.cpu.freeze()
        self.memory.clear()
        print("电脑已关闭")
        print("=" * 30)


if __name__ == "__main__":
    computer = ComputerFacade()
    computer.start()
    print()
    computer.shutdown()
