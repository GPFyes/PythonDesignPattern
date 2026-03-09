"""
建造者模式 - 入门级示例

简介：用最简单的方式演示建造者模式的核心思想
"""


class House:
    """产品：房子"""
    def __init__(self):
        self.walls = None
        self.roof = None
        self.windows = None
    
    def __str__(self):
        return f"House(walls={self.walls}, roof={self.roof}, windows={self.windows})"


class HouseBuilder:
    """建造者：构建房子"""
    def __init__(self):
        self.house = House()
    
    def build_walls(self, walls):
        self.house.walls = walls
        return self
    
    def build_roof(self, roof):
        self.house.roof = roof
        return self
    
    def build_windows(self, windows):
        self.house.windows = windows
        return self
    
    def get_result(self):
        return self.house


# 测试
if __name__ == "__main__":
    builder = HouseBuilder()
    house = builder.build_walls("Brick").build_roof("Tile").build_windows(4).get_result()
    print(house)
