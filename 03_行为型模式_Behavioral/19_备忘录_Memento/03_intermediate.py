"""
备忘录模式 - 中级
支持多个存档槽位和游戏章节的存档系统
"""

from datetime import datetime
from typing import Dict, Optional


class Item:
    """物品类"""

    def __init__(self, name: str, quantity: int = 1):
        self._name = name
        self._quantity = quantity

    @property
    def name(self) -> str:
        return self._name

    @property
    def quantity(self) -> int:
        return self._quantity

    def __str__(self) -> str:
        return f"{self._name}x{self._quantity}"


class Quest:
    """任务类"""

    def __init__(self, quest_id: str, title: str, completed: bool = False):
        self._quest_id = quest_id
        self._title = title
        self._completed = completed

    @property
    def quest_id(self) -> str:
        return self._quest_id

    @property
    def title(self) -> str:
        return self._title

    @property
    def completed(self) -> bool:
        return self._completed

    def complete(self):
        self._completed = True


class GameSnapshot:
    """备忘录：完整游戏快照"""

    def __init__(
        self,
        level: int,
        health: int,
        max_health: int,
        gold: int,
        chapter: str,
        items: list,
        quests: list
    ):
        self._level = level
        self._health = health
        self._max_health = max_health
        self._gold = gold
        self._chapter = chapter
        self._items = items
        self._quests = quests
        self._timestamp = datetime.now()

    @property
    def level(self) -> int:
        return self._level

    @property
    def health(self) -> int:
        return self._health

    @property
    def max_health(self) -> int:
        return self._max_health

    @property
    def gold(self) -> int:
        return self._gold

    @property
    def chapter(self) -> str:
        return self._chapter

    @property
    def items(self) -> list:
        return self._items

    @property
    def quests(self) -> list:
        return self._quests

    @property
    def timestamp(self) -> datetime:
        return self._timestamp


class RPGGame:
    """发起人：RPG游戏"""

    def __init__(self, player_name: str):
        self._player_name = player_name
        self._level = 1
        self._health = 100
        self._max_health = 100
        self._gold = 0
        self._chapter = "序章"
        self._items = []
        self._quests = []

    def play(self, chapter: str, exp_gain: int, gold_gain: int):
        self._chapter = chapter
        self._level += exp_gain // 100
        self._gold += gold_gain
        self._max_health += 10
        self._health = self._max_health
        print(f"\n=== 进入 {chapter} ===")

    def add_item(self, item: Item):
        for existing in self._items:
            if existing.name == item.name:
                existing._quantity += item._quantity
                return
        self._items.append(item)

    def remove_item(self, item_name: str, quantity: int = 1) -> bool:
        for item in self._items:
            if item.name == item_name:
                if item.quantity >= quantity:
                    item._quantity -= quantity
                    if item.quantity <= 0:
                        self._items.remove(item)
                    return True
        return False

    def add_quest(self, quest: Quest):
        self._quests.append(quest)

    def complete_quest(self, quest_id: str):
        for quest in self._quests:
            if quest.quest_id == quest_id:
                quest.complete()
                reward_gold = 500
                self._gold += reward_gold
                print(f"任务完成！获得 {reward_gold} 金币")

    def take_damage(self, damage: int):
        self._health -= damage

    def heal(self, amount: int):
        self._health = min(self._max_health, self._health + amount)

    def create_snapshot(self) -> GameSnapshot:
        items_copy = [Item(item.name, item.quantity) for item in self._items]
        quests_copy = [Quest(q.quest_id, q.title, q.completed) for q in self._quests]
        return GameSnapshot(
            self._level,
            self._health,
            self._max_health,
            self._gold,
            self._chapter,
            items_copy,
            quests_copy
        )

    def restore_snapshot(self, snapshot: GameSnapshot):
        self._level = snapshot.level
        self._health = snapshot.health
        self._max_health = snapshot.max_health
        self._gold = snapshot.gold
        self._chapter = snapshot.chapter
        self._items = [Item(item.name, item.quantity) for item in snapshot.items]
        self._quests = [Quest(q.quest_id, q.title, q.completed) for q in snapshot.quests]

    def show_status(self):
        print(f"\n玩家: {self._player_name}")
        print(f"等级: {self._level} | 章节: {self._chapter}")
        print(f"生命: {self._health}/{self._max_health} | 金币: {self._gold}")
        print(f"背包: {[str(item) for item in self._items]}")
        active_quests = [q for q in self._quests if not q.completed]
        if active_quests:
            print(f"任务: {[q.title for q in active_quests]}")


class SaveManager:
    """管理员：存档管理器"""

    def __init__(self, max_slots: int = 5):
        self._max_slots = max_slots
        self._saves: Dict[int, GameSnapshot] = {}

    def save(self, slot: int, snapshot: GameSnapshot) -> bool:
        if slot < 1 or slot > self._max_slots:
            print(f"无效的存档槽位 (1-{self._max_slots})")
            return False

        self._saves[slot] = snapshot
        print(f"✓ 存档已保存到槽位 {slot}")
        return True

    def load(self, slot: int) -> Optional[GameSnapshot]:
        if slot not in self._saves:
            print(f"槽位 {slot} 没有存档")
            return None
        print(f"正在从槽位 {slot} 读取存档...")
        return self._saves[slot]

    def delete(self, slot: int) -> bool:
        if slot in self._saves:
            del self._saves[slot]
            print(f"✓ 槽位 {slot} 的存档已删除")
            return True
        print(f"槽位 {slot} 没有存档")
        return False

    def list_saves(self):
        print("\n" + "=" * 40)
        print(f"存档列表 (共 {self._max_slots} 个槽位)")
        print("=" * 40)
        if not self._saves:
            print("暂无存档")
        else:
            for slot in range(1, self._max_slots + 1):
                if slot in self._saves:
                    s = self._saves[slot]
                    print(f"槽位 {slot}: [{s.chapter}] Lv.{s.level} | {s.gold}金币 | {s.timestamp.strftime('%Y-%m-%d %H:%M')}")
                else:
                    print(f"槽位 {slot}: [空]")
        print("=" * 40)


if __name__ == "__main__":
    game = RPGGame("主角")
    save_manager = SaveManager(max_slots=3)

    game.show_status()

    game.play("第一章：开始", 100, 200)
    game.add_item(Item("新手剑"))
    game.add_item(Item("血瓶", 3))
    game.add_quest(Quest("Q001", "击败史莱姆"))
    game.show_status()

    save_manager.save(1, game.create_snapshot())

    game.play("第二章：森林", 200, 300)
    game.add_item(Item("铁剑"))
    game.add_item(Item("魔法药水", 2))
    game.take_damage(30)
    game.complete_quest("Q001")
    game.show_status()

    save_manager.save(2, game.create_snapshot())

    print("\n" + "=" * 40)
    print("读取第一个存档")
    print("=" * 40)
    game.restore_snapshot(save_manager.load(1))
    game.show_status()

    save_manager.list_saves()
