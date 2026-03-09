"""
备忘录模式 - 高级
完整的游戏存档系统，支持自动保存、历史记录和云同步
"""

import json
import copy
from datetime import datetime
from typing import Dict, List, Optional, Callable
from abc import ABC, abstractmethod
from pathlib import Path


class Memento(ABC):
    """备忘录基类"""

    @abstractmethod
    def get_timestamp(self) -> datetime:
        pass

    @abstractmethod
    def get_label(self) -> str:
        pass


class Item:
    """物品"""

    def __init__(self, item_id: str, name: str, quantity: int = 1, level: int = 1):
        self._item_id = item_id
        self._name = name
        self._quantity = quantity
        self._level = level

    @property
    def item_id(self) -> str:
        return self._item_id

    @property
    def name(self) -> str:
        return self._name

    @property
    def quantity(self) -> int:
        return self._quantity

    @property
    def level(self) -> int:
        return self._level

    def to_dict(self) -> dict:
        return {
            "item_id": self._item_id,
            "name": self._name,
            "quantity": self._quantity,
            "level": self._level
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Item":
        return cls(
            data["item_id"],
            data["name"],
            data["quantity"],
            data.get("level", 1)
        )


class Quest:
    """任务"""

    def __init__(
        self,
        quest_id: str,
        title: str,
        description: str,
        completed: bool = False,
        progress: int = 0,
        target: int = 1
    ):
        self._quest_id = quest_id
        self._title = title
        self._description = description
        self._completed = completed
        self._progress = progress
        self._target = target

    @property
    def quest_id(self) -> str:
        return self._quest_id

    @property
    def title(self) -> str:
        return self._title

    @property
    def completed(self) -> bool:
        return self._completed

    @property
    def progress(self) -> int:
        return self._progress

    def update_progress(self, amount: int = 1):
        self._progress += amount
        if self._progress >= self._target:
            self._completed = True

    def to_dict(self) -> dict:
        return {
            "quest_id": self._quest_id,
            "title": self._title,
            "description": self._description,
            "completed": self._completed,
            "progress": self._progress,
            "target": self._target
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Quest":
        return cls(
            data["quest_id"],
            data["title"],
            data["description"],
            data["completed"],
            data["progress"],
            data["target"]
        )


class Skill:
    """技能"""

    def __init__(self, skill_id: str, name: str, level: int = 1, cooldown: int = 0):
        self._skill_id = skill_id
        self._name = name
        self._level = level
        self._cooldown = cooldown

    @property
    def skill_id(self) -> str:
        return self._skill_id

    @property
    def name(self) -> str:
        return self._name

    @property
    def level(self) -> int:
        return self._level

    def to_dict(self) -> dict:
        return {
            "skill_id": self._skill_id,
            "name": self._name,
            "level": self._level,
            "cooldown": self._cooldown
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Skill":
        return cls(
            data["skill_id"],
            data["name"],
            data["level"],
            data["cooldown"]
        )


class GameSnapshot(Memento):
    """游戏快照 - 备忘录实现"""

    def __init__(
        self,
        player_name: str,
        level: int,
        experience: int,
        health: int,
        max_health: int,
        mana: int,
        max_mana: int,
        gold: int,
        chapter: str,
        location: str,
        items: List[Item],
        quests: List[Quest],
        skills: List[Skill],
        play_time: int,
        label: str = "自动存档"
    ):
        self._player_name = player_name
        self._level = level
        self._experience = experience
        self._health = health
        self._max_health = max_health
        self._mana = mana
        self._max_mana = max_mana
        self._gold = gold
        self._chapter = chapter
        self._location = location
        self._items = items
        self._quests = quests
        self._skills = skills
        self._play_time = play_time
        self._timestamp = datetime.now()
        self._label = label

    def get_timestamp(self) -> datetime:
        return self._timestamp

    def get_label(self) -> str:
        return self._label

    @property
    def player_name(self) -> str:
        return self._player_name

    @property
    def level(self) -> int:
        return self._level

    @property
    def experience(self) -> int:
        return self._experience

    @property
    def health(self) -> int:
        return self._health

    @property
    def gold(self) -> int:
        return self._gold

    @property
    def chapter(self) -> str:
        return self._chapter

    @property
    def location(self) -> str:
        return self._location

    @property
    def items(self) -> List[Item]:
        return self._items

    @property
    def quests(self) -> List[Quest]:
        return self._quests

    @property
    def skills(self) -> List[Skill]:
        return self._skills

    @property
    def play_time(self) -> int:
        return self._play_time

    def to_dict(self) -> dict:
        return {
            "player_name": self._player_name,
            "level": self._level,
            "experience": self._experience,
            "health": self._health,
            "max_health": self._max_health,
            "mana": self._mana,
            "max_mana": self._max_mana,
            "gold": self._gold,
            "chapter": self._chapter,
            "location": self._location,
            "items": [item.to_dict() for item in self._items],
            "quests": [quest.to_dict() for quest in self._quests],
            "skills": [skill.to_dict() for skill in self._skills],
            "play_time": self._play_time,
            "timestamp": self._timestamp.isoformat(),
            "label": self._label
        }

    @classmethod
    def from_dict(cls, data: dict) -> "GameSnapshot":
        snapshot = cls(
            player_name=data["player_name"],
            level=data["level"],
            experience=data["experience"],
            health=data["health"],
            max_health=data["max_health"],
            mana=data["mana"],
            max_mana=data["max_mana"],
            gold=data["gold"],
            chapter=data["chapter"],
            location=data["location"],
            items=[Item.from_dict(i) for i in data["items"]],
            quests=[Quest.from_dict(q) for q in data["quests"]],
            skills=[Skill.from_dict(s) for s in data["skills"]],
            play_time=data["play_time"],
            label=data["label"]
        )
        return snapshot


class RPGGame:
    """发起人：RPG游戏"""

    def __init__(self, player_name: str):
        self._player_name = player_name
        self._level = 1
        self._experience = 0
        self._health = 100
        self._max_health = 100
        self._mana = 50
        self._max_mana = 50
        self._gold = 0
        self._chapter = "序章"
        self._location = "新手村"
        self._items: List[Item] = []
        self._quests: List[Quest] = []
        self._skills: List[Skill] = []
        self._play_time = 0
        self._save_hooks: List[Callable] = []
        self._load_hooks: List[Callable] = []

    def register_save_hook(self, hook: Callable):
        self._save_hooks.append(hook)

    def register_load_hook(self, hook: Callable):
        self._load_hooks.append(hook)

    def play(self, chapter: str, location: str):
        self._chapter = chapter
        self._location = location

    def gain_experience(self, amount: int):
        self._experience += amount
        while self._experience >= self._level * 100:
            self._experience -= self._level * 100
            self._level += 1
            self._max_health += 10
            self._max_mana += 5
            self._health = self._max_health
            self._mana = self._max_mana
            print(f"*** 升级！现在是 {self._level} 级 ***")

    def add_gold(self, amount: int):
        self._gold += amount

    def spend_gold(self, amount: int) -> bool:
        if self._gold >= amount:
            self._gold -= amount
            return True
        return False

    def take_damage(self, damage: int):
        self._health = max(0, self._health - damage)

    def use_mana(self, cost: int) -> bool:
        if self._mana >= cost:
            self._mana -= cost
            return True
        return False

    def heal(self, amount: int):
        self._health = min(self._max_health, self._health + amount)

    def restore_mana(self, amount: int):
        self._mana = min(self._max_mana, self._mana + amount)

    def add_item(self, item: Item):
        for existing in self._items:
            if existing.item_id == item.item_id:
                existing._quantity += item._quantity
                return
        self._items.append(item)

    def remove_item(self, item_id: str, quantity: int = 1) -> bool:
        for item in self._items:
            if item.item_id == item_id:
                if item.quantity >= quantity:
                    item._quantity -= quantity
                    if item.quantity <= 0:
                        self._items.remove(item)
                    return True
        return False

    def add_quest(self, quest: Quest):
        self._quests.append(quest)

    def update_quest(self, quest_id: str, progress: int = 1):
        for quest in self._quests:
            if quest.quest_id == quest_id and not quest.completed:
                quest.update_progress(progress)
                return True
        return False

    def learn_skill(self, skill: Skill):
        for existing in self._skills:
            if existing.skill_id == skill.skill_id:
                existing._level += 1
                return
        self._skills.append(skill)

    def add_play_time(self, seconds: int):
        self._play_time += seconds

    def create_snapshot(self, label: str = "手动存档") -> GameSnapshot:
        snapshot = GameSnapshot(
            player_name=self._player_name,
            level=self._level,
            experience=self._experience,
            health=self._health,
            max_health=self._max_health,
            mana=self._mana,
            max_mana=self._max_mana,
            gold=self._gold,
            chapter=self._chapter,
            location=self._location,
            items=copy.deepcopy(self._items),
            quests=copy.deepcopy(self._quests),
            skills=copy.deepcopy(self._skills),
            play_time=self._play_time,
            label=label
        )
        for hook in self._save_hooks:
            hook(snapshot)
        return snapshot

    def restore_snapshot(self, snapshot: GameSnapshot):
        self._player_name = snapshot.player_name
        self._level = snapshot.level
        self._experience = snapshot.experience
        self._health = snapshot.health
        self._max_health = snapshot.max_health
        self._mana = snapshot.mana
        self._max_mana = snapshot.max_mana
        self._gold = snapshot.gold
        self._chapter = snapshot.chapter
        self._location = snapshot.location
        self._items = copy.deepcopy(snapshot.items)
        self._quests = copy.deepcopy(snapshot.quests)
        self._skills = copy.deepcopy(snapshot.skills)
        self._play_time = snapshot.play_time
        for hook in self._load_hooks:
            hook(snapshot)

    def show_status(self):
        print(f"\n{'=' * 50}")
        print(f"玩家: {self._player_name}")
        print(f"等级: {self._level} | 经验: {self._experience}/{self._level * 100}")
        print(f"章节: {self._chapter} | 地点: {self._location}")
        print(f"生命: {self._health}/{self._max_health} | 法力: {self._mana}/{self._max_mana}")
        print(f"金币: {self._gold}")
        print(f"背包: {len(self._items)} 个物品")
        active = [q for q in self._quests if not q.completed]
        if active:
            print(f"任务: {len(active)} 个进行中")
        print(f"已玩时间: {self._play_time} 秒")
        print(f"{'=' * 50}")


class SaveManager:
    """管理员：存档管理器"""

    def __init__(self, max_slots: int = 10, auto_save_count: int = 3):
        self._max_slots = max_slots
        self._auto_save_count = auto_save_count
        self._saves: Dict[int, GameSnapshot] = {}
        self._auto_saves: List[GameSnapshot] = []
        self._history: List[GameSnapshot] = []
        self._max_history = 20
        self._cloud_enabled = False
        self._cloud_callbacks: List[Callable] = []

    def enable_cloud_sync(self, callback: Callable):
        self._cloud_enabled = True
        self._cloud_callbacks.append(callback)

    def save(self, slot: int, snapshot: GameSnapshot) -> bool:
        if slot < 1 or slot > self._max_slots:
            print(f"无效的存档槽位 (1-{self._max_slots})")
            return False
        self._saves[slot] = snapshot
        self._add_to_history(snapshot)
        self._sync_to_cloud(snapshot)
        print(f"✓ 存档已保存到槽位 {slot}: {snapshot.get_label()}")
        return True

    def load(self, slot: int) -> Optional[GameSnapshot]:
        if slot not in self._saves:
            print(f"槽位 {slot} 没有存档")
            return None
        snapshot = self._saves[slot]
        self._add_to_history(snapshot)
        print(f"✓ 从槽位 {slot} 读取存档: {snapshot.get_label()}")
        return snapshot

    def auto_save(self, snapshot: GameSnapshot) -> bool:
        self._auto_saves.append(snapshot)
        if len(self._auto_saves) > self._auto_save_count:
            self._auto_saves.pop(0)
        self._add_to_history(snapshot)
        self._sync_to_cloud(snapshot)
        print(f"✓ 自动存档完成: {snapshot.get_label()}")
        return True

    def load_auto_save(self, index: int = -1) -> Optional[GameSnapshot]:
        if not self._auto_saves:
            print("没有自动存档")
            return None
        snapshot = self._auto_saves[index]
        self._add_to_history(snapshot)
        print(f"✓ 读取自动存档: {snapshot.get_label()}")
        return snapshot

    def delete(self, slot: int) -> bool:
        if slot in self._saves:
            del self._saves[slot]
            print(f"✓ 槽位 {slot} 的存档已删除")
            return True
        print(f"槽位 {slot} 没有存档")
        return False

    def _add_to_history(self, snapshot: GameSnapshot):
        self._history.append(snapshot)
        if len(self._history) > self._max_history:
            self._history.pop(0)

    def undo(self) -> Optional[GameSnapshot]:
        if len(self._history) < 2:
            print("没有可撤销的存档")
            return None
        self._history.pop()
        snapshot = self._history[-1]
        print(f"✓ 撤销到上一个存档: {snapshot.get_label()}")
        return snapshot

    def _sync_to_cloud(self, snapshot: GameSnapshot):
        if self._cloud_enabled:
            for callback in self._cloud_callbacks:
                callback(snapshot)

    def export_to_file(self, filepath: str, slot: int) -> bool:
        if slot not in self._saves:
            print(f"槽位 {slot} 没有存档")
            return False
        try:
            data = self._saves[slot].to_dict()
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"✓ 存档已导出到 {filepath}")
            return True
        except Exception as e:
            print(f"导出失败: {e}")
            return False

    def import_from_file(self, filepath: str) -> Optional[GameSnapshot]:
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
            snapshot = GameSnapshot.from_dict(data)
            print(f"✓ 从 {filepath} 导入存档")
            return snapshot
        except Exception as e:
            print(f"导入失败: {e}")
            return None

    def list_saves(self):
        print("\n" + "=" * 60)
        print(f"存档列表 (槽位 1-{self._max_slots})")
        print("=" * 60)
        for slot in range(1, self._max_slots + 1):
            if slot in self._saves:
                s = self._saves[slot]
                print(f"槽位 {slot}: [{s.chapter}] Lv.{s.level} | {s.gold}G | {s.get_label()} | {s.get_timestamp().strftime('%Y-%m-%d %H:%M')}")
            else:
                print(f"槽位 {slot}: [空]")
        print("-" * 60)
        print(f"自动存档 ({len(self._auto_saves)}/{self._auto_save_count}):")
        for i, s in enumerate(self._auto_saves):
            print(f"  自动{i + 1}: [{s.chapter}] Lv.{s.level} | {s.get_label()}")
        print("=" * 60)


def cloud_sync_callback(snapshot: GameSnapshot):
    print(f"[云同步] 存档已同步: {snapshot.get_label()}")


if __name__ == "__main__":
    game = RPGGame("冒险者")
    save_manager = SaveManager(max_slots=5, auto_save_count=3)
    save_manager.enable_cloud_sync(cloud_sync_callback)

    game.play("第一章：觉醒", "新手村")
    game.gain_experience(150)
    game.add_gold(100)
    game.add_item(Item("I001", "新手剑", 1, 1))
    game.add_quest(Quest("Q001", "击败史莱姆", "在新手村击败5只史莱姆", False, 0, 5))
    game.show_status()

    save_manager.auto_save(game.create_snapshot("自动存档1"))

    game.play("第二章：冒险", "森林")
    game.add_item(Item("I002", "皮甲", 1, 2))
    game.update_quest("Q001", 2)
    game.take_damage(20)
    game.show_status()

    save_manager.auto_save(game.create_snapshot("自动存档2"))

    game.play("第三章：挑战", "山洞")
    game.add_item(Item("I003", "铁剑", 1, 3))
    game.add_gold(500)
    game.update_quest("Q001", 3)
    game.show_status()

    save_manager.save(1, game.create_snapshot("主存档"))

    print("\n" + "=" * 60)
    print("读取自动存档1")
    print("=" * 60)
    game.restore_snapshot(save_manager.load_auto_save(0))
    game.show_status()

    print("\n" + "=" * 60)
    print("读取主存档")
    print("=" * 60)
    game.restore_snapshot(save_manager.load(1))
    game.show_status()

    save_manager.list_saves()

    print("\n测试云同步...")
    test_snapshot = game.create_snapshot("云测试")
    save_manager._sync_to_cloud(test_snapshot)
