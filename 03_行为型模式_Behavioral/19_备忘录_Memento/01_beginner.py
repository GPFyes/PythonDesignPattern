"""
备忘录模式 - 入门级
游戏存档基础示例
"""


class GameMemento:
    """备忘录：存储游戏状态"""

    def __init__(self, level: int, health: int, gold: int):
        self._level = level
        self._health = health
        self._gold = gold

    def get_level(self) -> int:
        return self._level

    def get_health(self) -> int:
        return self._health

    def get_gold(self) -> int:
        return self._gold


class Game:
    """发起人：游戏对象"""

    def __init__(self):
        self._level = 1
        self._health = 100
        self._gold = 0

    def play(self):
        self._level += 1
        self._health -= 10
        self._gold += 100
        print(f"游戏中... 关卡: {self._level}, 生命: {self._health}, 金币: {self._gold}")

    def save(self) -> GameMemento:
        return GameMemento(self._level, self._health, self._gold)

    def restore(self, memento: GameMemento):
        self._level = memento.get_level()
        self._health = memento.get_health()
        self._gold = memento.get_gold()
        print(f"读档成功! 关卡: {self._level}, 生命: {self._health}, 金币: {self._gold}")

    def show_status(self):
        print(f"当前状态 - 关卡: {self._level}, 生命: {self._health}, 金币: {self._gold}")


class GameCaretaker:
    """管理员：管理存档"""

    def __init__(self):
        self._memento = None

    def save_game(self, memento: GameMemento):
        self._memento = memento
        print("存档已保存")

    def load_game(self) -> GameMemento:
        if self._memento:
            print("读取存档中...")
            return self._memento
        return None


if __name__ == "__main__":
    game = Game()
    caretaker = GameCaretaker()

    game.show_status()

    print("\n--- 第一次游戏 ---")
    game.play()
    game.play()

    caretaker.save_game(game.save())

    print("\n--- 第二次游戏 ---")
    game.play()
    game.play()
    game.show_status()

    print("\n--- 读取存档 ---")
    game.restore(caretaker.load_game())
