"""外观模式 - 入门级示例"""


class CPU:
    def process(self):
        print("CPU处理中")


class Memory:
    def load(self):
        print("内存加载数据")


class ComputerFacade:
    def __init__(self):
        self.cpu = CPU()
        self.memory = Memory()

    def start(self):
        self.memory.load()
        self.cpu.process()
        print("电脑启动完成")


if __name__ == "__main__":
    ComputerFacade().start()
