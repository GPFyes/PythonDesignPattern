"""
原型模式 - 中级示例

简介：展示游戏中的角色克隆应用
"""

import copy
from typing import List


class GameCharacter:
    """游戏角色"""
    def __init__(self, name, hp, mp, skills=None):
        self.name = name
        self.hp = hp
        self.mp = mp
        self.skills = skills or []
    
    def clone(self):
        return copy.deepcopy(self)
    
    def __str__(self):
        return f"{self.name}(HP={self.hp}, MP={self.mp}, 技能={self.skills})"


class CharacterFactory:
    """角色工厂，保存原型"""
    def __init__(self):
        self.prototypes = {}
    
    def register(self, name, character):
        self.prototypes[name] = character
    
    def create(self, name):
        return self.prototypes[name].clone()


if __name__ == "__main__":
    factory = CharacterFactory()
    
    warrior = GameCharacter("战士", 100, 50, ["冲锋", "斩击"])
    mage = GameCharacter("法师", 60, 100, ["火球", "冰霜"])
    
    factory.register("warrior", warrior)
    factory.register("mage", mage)
    
    player1 = factory.create("warrior")
    player1.name = "玩家1"
    print(player1)
    
    player2 = factory.create("mage")
    player2.name = "玩家2"
    print(player2)
