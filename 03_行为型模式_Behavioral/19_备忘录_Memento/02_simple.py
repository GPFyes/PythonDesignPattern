"""
备忘录模式 - 简单级
带存档槽位的游戏存档系统
"""


from datetime import datetime


class GameState:
    """备忘录：存储游戏状态"""

    def __init__(self, level: int, health: int, gold: int, inventory: list):
        self._level = level
        self._health = health
        self._gold = gold
        self._inventory = inventory
        self._timestamp = datetime.now()

    @property
    def level(self) -> int:
        return self._level

    @property
    def health(self) -> int:
        return self._health

    @property
    def gold(self) -> int:
        return self._gold

    @property
    def inventory(self) -> list:
        return self._inventory

    @property
    def timestamp(self) -> datetime:
        return self._timestamp


class GameCharacter:
    """发起人：游戏角色"""

    def __init__(self, name: str):
        self._name = name
        self._level = 1
        self._health = 100
        self._gold = 0
        self._inventory = []

    def gain_experience(self, exp: int):
        self._level += exp // 100
        self._health = min(100, self._health + 10)
        self._gold += exp

    def spend_gold(self, amount: int) -> bool:
        if self._gold >= amount:
            self._gold -= amount
            return True
        return False

    def add_item(self, item: str):
        self._inventory.append(item)

    def take_damage(self, damage: int):
        self._health -= damage
        if self._health < 0:
            self._health = 0

    def save_state(self) -> GameState:
        return GameState(
            self._level,
            self._health,
            self._gold,
            self._inventory.copy()
        )

    def load_state(self, state: GameState):
        self._level = state.level
        self._health = state.health
        self._gold = state.gold
        self._inventory = state.inventory.copy()

    def show_status(self):
        print(f"【{self._name}】等级: {self._level}, 生命: {self._health}, 金币: {self._gold}")
        print(f"   背包: {', '.join(self._inventory) if self._inventory else '空'}")


class SaveManager:
    """管理员：管理多个存档槽位"""

    def __init__(self):
        self._saves = {}

    def save(self, slot: int, state: GameState):
        self._saves[slot] = state
        print(f"存档已保存到槽位 {slot}")

    def load(self, slot: int) -> GameState:
        if slot in self._saves:
            return self._saves[slot]
        return None

    def list_saves(self):
        if not self._saves:
            print("暂无存档")
        else:
            print("存档列表:")
            for slot, state in self._saves.items():
                print(f"  槽位 {slot}: 等级{state.level} | 金币{state.gold} | {state.timestamp.strftime('%H:%M:%S')}")

    def delete(self, slot: int):
        if slot in self._saves:
            del self._saves[slot]
            print(f"槽位 {slot} 的存档已删除")


if __name__ == "__main__":
    player = GameCharacter("勇者")
    save_manager = SaveManager()

    player.show_status()

    print("\n=== 第一章：新手村 ===")
    player.gain_experience(150)
    player.add_item("新手剑")
    player.add_item("血瓶")
    player.show_status()

    save_manager.save(1, player.save_state())

    print("\n=== 第二章：森林 ===")
    player.gain_experience(200)
    player.add_item("森林地图")
    player.spend_gold(50)
    player.take_damage(30)
    player.show_status()

    print("\n=== 读取存档 ===")
    save_manager.load(1)
    player.load_state(save_manager.load(1))
    player.show_status()

    print("\n=== 存档列表 ===")
    save_manager.list_saves()
