"""
建造者模式 - 中级示例

简介：实际场景，展示构建复杂对象
"""


class Computer:
    """产品：电脑"""
    def __init__(self):
        self.cpu = None
        self.memory = None
        self.storage = None
        self.graphics_card = None
    
    def __str__(self):
        return (f"Computer(cpu={self.cpu}, memory={self.memory}, "
                f"storage={self.storage}, graphics_card={self.graphics_card})")


class ComputerBuilder:
    """电脑建造者"""
    def __init__(self):
        self.computer = Computer()
    
    def build_cpu(self, cpu):
        self.computer.cpu = cpu
        return self
    
    def build_memory(self, memory):
        self.computer.memory = memory
        return self
    
    def build_storage(self, storage):
        self.computer.storage = storage
        return self
    
    def build_graphics_card(self, card):
        self.computer.graphics_card = card
        return self
    
    def get_result(self):
        return self.computer


class Director:
    """指挥者：预设配置"""
    def __init__(self, builder: ComputerBuilder):
        self.builder = builder
    
    def build_office_pc(self):
        return (self.builder
            .build_cpu("Intel i5")
            .build_memory("8GB")
            .build_storage("256GB SSD")
            .build_graphics_card("集成显卡")
            .get_result())
    
    def build_gaming_pc(self):
        return (self.builder
            .build_cpu("Intel i9")
            .build_memory("64GB")
            .build_storage("2TB SSD")
            .build_graphics_card("RTX 4090")
            .get_result())


if __name__ == "__main__":
    director = Director(ComputerBuilder())
    
    office = director.build_office_pc()
    print("办公电脑:", office)
    
    gaming = director.build_gaming_pc()
    print("游戏电脑:", gaming)
