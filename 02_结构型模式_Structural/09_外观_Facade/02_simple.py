"""外观模式 - 简单级示例"""


class CPU:
    def process(self):
        print("CPU: 处理器初始化")
        print("CPU: 执行计算任务")


class Memory:
    def load(self):
        print("Memory: 加载BIOS")
        print("Memory: 加载操作系统")


class Disk:
    def read(self):
        print("Disk: 读取启动扇区")


class Computer:
    def __init__(self):
        self.cpu = CPU()
        self.memory = Memory()
        self.disk = Disk()

    def start(self):
        print("=== 电脑启动 ===")
        self.disk.read()
        self.memory.load()
        self.cpu.process()
        print("=== 启动完成 ===")

    def shutdown(self):
        print("=== 电脑关闭 ===")
        self.cpu.process = lambda: print("CPU: 停止计算")
        self.memory.load = lambda: print("Memory: 清理数据")
        self.cpu.process()
        self.memory.load()
        print("=== 关闭完成 ===")


if __name__ == "__main__":
    computer = Computer()
    computer.start()
    print()
    computer.shutdown()
