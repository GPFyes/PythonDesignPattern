"""
抽象工厂模式 - 高级示例

简介：生产级实现，展示游戏开发中的应用
"""

from abc import ABC, abstractmethod
from typing import Dict, Any


# 抽象产品：武器
class Weapon(ABC):
    @abstractmethod
    def attack(self) -> str:
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        pass


# 抽象产品：护甲
class Armor(ABC):
    @abstractmethod
    def defend(self) -> int:
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        pass


# 抽象产品：坐骑
class Mount(ABC):
    @abstractmethod
    def ride(self) -> str:
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        pass


# ===== 森林王国产品族 =====
class ForestSword(Weapon):
    def __init__(self):
        self.name = "森林之剑"
        self.damage = 50
    
    def attack(self) -> str:
        return f"{self.name} 发出绿光，攻击力 {self.damage}"
    
    def get_name(self) -> str:
        return self.name


class ForestArmor(Armor):
    def __init__(self):
        self.name = "森林护甲"
        self.defense = 30
    
    def defend(self) -> int:
        return self.defense
    
    def get_name(self) -> str:
        return self.name


class ForestMount(Mount):
    def __init__(self):
        self.name = "森林麋鹿"
        self.speed = 80
    
    def ride(self) -> str:
        return f"骑上{self.name}，速度 {self.speed}"
    
    def get_name(self) -> str:
        return self.name


# ===== 火焰王国产品族 =====
class FireSword(Weapon):
    def __init__(self):
        self.name = "火焰之剑"
        self.damage = 70
    
    def attack(self) -> str:
        return f"{self.name} 火焰燃烧，攻击力 {self.damage}"
    
    def get_name(self) -> str:
        return self.name


class FireArmor(Armor):
    def __init__(self):
        self.name = "火焰护甲"
        self.defense = 25
    
    def defend(self) -> int:
        return self.defense
    
    def get_name(self) -> str:
        return self.name


class FireMount(Mount):
    def __init__(self):
        self.name = "火焰战马"
        self.speed = 100
    
    def ride(self) -> str:
        return f"骑上{self.name}，速度 {self.speed}"
    
    def get_name(self) -> str:
        return self.name


# ===== 冰霜王国产品族 =====
class IceSword(Weapon):
    def __init__(self):
        self.name = "冰霜之剑"
        self.damage = 60
    
    def attack(self) -> str:
        return f"{self.name} 寒气逼人，攻击力 {self.damage}"
    
    def get_name(self) -> str:
        return self.name


class IceArmor(Armor):
    def __init__(self):
        self.name = "冰霜护甲"
        self.defense = 35
    
    def defend(self) -> int:
        return self.defense
    
    def get_name(self) -> str:
        return self.name


class IceMount(Mount):
    def __init__(self):
        self.name = "冰霜巨狼"
        self.speed = 90
    
    def ride(self) -> str:
        return f"骑上{self.name}，速度 {self.speed}"
    
    def get_name(self) -> str:
        return self.name


# 抽象工厂
class KingdomFactory(ABC):
    @abstractmethod
    def create_weapon(self) -> Weapon:
        pass
    
    @abstractmethod
    def create_armor(self) -> Armor:
        pass
    
    @abstractmethod
    def create_mount(self) -> Mount:
        pass
    
    @abstractmethod
    def get_kingdom_name(self) -> str:
        pass


# 具体工厂
class ForestKingdomFactory(KingdomFactory):
    def create_weapon(self) -> Weapon:
        return ForestSword()
    
    def create_armor(self) -> Armor:
        return ForestArmor()
    
    def create_mount(self) -> Mount:
        return ForestMount()
    
    def get_kingdom_name(self) -> str:
        return "森林王国"


class FireKingdomFactory(KingdomFactory):
    def create_weapon(self) -> Weapon:
        return FireSword()
    
    def create_armor(self) -> Armor:
        return FireArmor()
    
    def create_mount(self) -> Mount:
        return FireMount()
    
    def get_kingdom_name(self) -> str:
        return "火焰王国"


class IceKingdomFactory(KingdomFactory):
    def create_weapon(self) -> Weapon:
        return IceSword()
    
    def create_armor(self) -> Armor:
        return IceArmor()
    
    def create_mount(self) -> Mount:
        return IceMount()
    
    def get_kingdom_name(self) -> str:
        return "冰霜王国"


class Character:
    """游戏角色"""
    
    def __init__(self, name: str, factory: KingdomFactory):
        self.name = name
        self.factory = factory
        self.weapon = factory.create_weapon()
        self.armor = factory.create_armor()
        self.mount = factory.create_mount()
    
    def show_equipment(self):
        """展示装备"""
        print(f"\n{self.name} 的装备 ({self.factory.get_kingdom_name()})")
        print(f"  武器: {self.weapon.get_name()}")
        print(f"  护甲: {self.armor.get_name()}")
        print(f"  坐骑: {self.mount.get_name()}")
    
    def attack(self):
        """攻击"""
        print(f"\n{self.name} 攻击: {self.weapon.attack()}")
    
    def defend(self):
        """防御"""
        print(f"{self.name} 防御: 护甲提供 {self.armor.defend()} 点防御")
    
    def ride_mount(self):
        """骑乘坐骑"""
        print(f"{self.name} {self.mount.ride()}")


def main():
    """测试抽象工厂模式 - 游戏装备"""
    print("=" * 60)
    print("抽象工厂模式 - 游戏装备系统")
    print("=" * 60)
    
    # 创建不同王国的角色
    forest_hero = Character("森林英雄", ForestKingdomFactory())
    fire_hero = Character("火焰英雄", FireKingdomFactory())
    ice_hero = Character("冰霜英雄", IceKingdomFactory())
    
    # 展示装备
    for hero in [forest_hero, fire_hero, ice_hero]:
        hero.show_equipment()
        hero.attack()
        hero.defend()
        hero.ride_mount()
    
    print("\n" + "=" * 60)
    print("说明：")
    print("- 每个王国是一完整的产品族")
    print("- 切换工厂即可切换整个装备体系")
    print("- 符合开闭原则，便于扩展新王国")
    print("=" * 60)


if __name__ == "__main__":
    main()
