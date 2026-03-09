from abc import ABC, abstractmethod


class Flyweight(ABC):
    @abstractmethod
    def operation(self, extrinsic_state):
        pass


class ConcreteFlyweight(Flyweight):
    def __init__(self, intrinsic_state):
        self._intrinsic_state = intrinsic_state

    def operation(self, extrinsic_state):
        return f"内部状态:{self._intrinsic_state}, 外部状态:{extrinsic_state}"


class UnsharedConcreteFlyweight(Flyweight):
    def __init__(self, all_state):
        self._all_state = all_state

    def operation(self, extrinsic_state):
        return f"所有状态:{self._all_state}, 外部状态:{extrinsic_state}"


class FlyweightFactory:
    _flyweights = {}

    @classmethod
    def get_flyweight(cls, key):
        if key not in cls._flyweights:
            cls._flyweights[key] = ConcreteFlyweight(key)
        return cls._flyweights[key]

    @classmethod
    def count(cls):
        return len(cls._flyweights)


if __name__ == "__main__":
    f1 = FlyweightFactory.get_flyweight("A")
    f2 = FlyweightFactory.get_flyweight("B")
    f3 = FlyweightFactory.get_flyweight("A")

    print(f1.operation("外部1"))
    print(f2.operation("外部2"))
    print(f3.operation("外部3"))
    print(f"共享对象数量:{FlyweightFactory.count()}")
    print(f"f1和f3是同一对象:{f1 is f3}")
