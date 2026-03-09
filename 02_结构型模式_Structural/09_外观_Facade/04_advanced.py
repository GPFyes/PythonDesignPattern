"""外观模式 - 高级示例"""


class CPU:
    def __init__(self):
        self.state = "off"
        self.clock_speed = 0

    def start(self):
        print("[CPU] 初始化处理器...")
        self.state = "on"
        self.clock_speed = 3600
        print(f"[CPU] 时钟频率: {self.clock_speed}MHz")

    def stop(self):
        print("[CPU] 停止处理器...")
        self.state = "off"
        self.clock_speed = 0


class Memory:
    def __init__(self):
        self.state = "off"
        self.capacity = 0
        self.data = {}

    def start(self):
        print("[Memory] 初始化内存控制器...")
        self.state = "on"
        self.capacity = 16
        print(f"[Memory] 容量: {self.capacity}GB")

    def stop(self):
        print("[Memory] 关闭内存控制器...")
        self.state = "off"

    def load(self, address, data):
        self.data[address] = data
        print(f"[Memory] 加载数据到地址 0x{address:08x}")


class Disk:
    def __init__(self):
        self.state = "off"
        self.capacity = 0

    def start(self):
        print("[Disk] 初始化磁盘控制器...")
        self.state = "on"
        self.capacity = 512
        print(f"[Disk] 容量: {self.capacity}GB")

    def stop(self):
        print("[Disk] 关闭磁盘控制器...")
        self.state = "off"

    def read_boot_sector(self):
        print("[Disk] 读取启动扇区...")
        return "boot_loader_v1.0"


class ComputerFacade:
    def __init__(self):
        self.cpu = CPU()
        self.memory = Memory()
        self.disk = Disk()
        self.is_running = False

    def boot(self):
        if self.is_running:
            print("电脑已经在运行中")
            return
        print("=" * 40)
        print("正在启动电脑...")
        print("=" * 40)
        self.disk.start()
        boot_data = self.disk.read_boot_sector()
        self.memory.start()
        self.memory.load(0xFFFF0000, boot_data)
        self.cpu.start()
        self.is_running = True
        print("=" * 40)
        print("电脑启动完成!")
        print("=" * 40)

    def shutdown(self):
        if not self.is_running:
            print("电脑已经关闭")
            return
        print("=" * 40)
        print("正在关闭电脑...")
        print("=" * 40)
        self.cpu.stop()
        self.memory.stop()
        self.disk.stop()
        self.is_running = False
        print("=" * 40)
        print("电脑已关闭!")
        print("=" * 40)


if __name__ == "__main__":
    computer = ComputerFacade()
    computer.boot()
    print()
    computer.shutdown()
