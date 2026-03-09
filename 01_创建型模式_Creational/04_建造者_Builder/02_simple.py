"""
建造者模式 - 简单级示例

简介：完整的建造者模式实现，展示链式调用
"""


class House:
    """产品：房子"""
    def __init__(self):
        self.walls = None
        self.roof = None
        self.windows = None
        self.door = None
        self.garage = None
    
    def __str__(self):
        return f"House(walls={self.walls}, roof={self.roof}, windows={self.windows}, door={self.door}, garage={self.garage})"


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
    
    def build_door(self, door):
        self.house.door = door
        return self
    
    def build_garage(self, garage):
        self.house.garage = garage
        return self
    
    def get_result(self):
        return self.house


class Director:
    """指挥者：指导建造过程"""
    def __init__(self, builder: HouseBuilder):
        self.builder = builder
    
    def build_basic_house(self):
        """建造简单房子"""
        return self.builder.build_walls("砖墙").build_roof("瓦片屋顶").get_result()
    
    def build_full_house(self):
        """建造完整房子"""
        return (self.builder
            .build_walls("钢筋混凝土墙")
            .build_roof("豪华屋顶")
            .build_windows(6)
            .build_door("防盗门")
            .build_garage("双车库")
            .get_result())


if __name__ == "__main__":
    # 使用指挥者
    director = Director(HouseBuilder())
    basic = director.build_basic_house()
    print("简单房子:", basic)
    
    full = HouseBuilder().build_walls("砖墙").build_roof("瓦片").build_windows(4).get_result()
    print("自定义房子:", full)
