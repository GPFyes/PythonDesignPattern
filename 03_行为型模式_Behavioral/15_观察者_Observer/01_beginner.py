from abc import ABC, abstractmethod
from typing import List


class Observer(ABC):
    @abstractmethod
    def update(self, temperature: float) -> None:
        pass


class Subject(ABC):
    @abstractmethod
    def attach(self, observer: Observer) -> None:
        pass

    @abstractmethod
    def detach(self, observer: Observer) -> None:
        pass

    @abstractmethod
    def notify(self) -> None:
        pass


class WeatherStation(Subject):
    def __init__(self) -> None:
        self._observers: List[Observer] = []
        self._temperature: float = 0.0

    def attach(self, observer: Observer) -> None:
        self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        self._observers.remove(observer)

    def notify(self) -> None:
        for observer in self._observers:
            observer.update(self._temperature)

    def set_temperature(self, temperature: float) -> None:
        print(f"气象站: 温度变化为 {temperature}°C")
        self._temperature = temperature
        self.notify()


class TemperatureDisplay(Observer):
    def __init__(self, name: str) -> None:
        self.name = name

    def update(self, temperature: float) -> None:
        print(f"{self.name}: 当前温度 {temperature}°C")


if __name__ == "__main__":
    weather_station = WeatherStation()

    display1 = TemperatureDisplay("显示器A")
    display2 = TemperatureDisplay("显示器B")

    weather_station.attach(display1)
    weather_station.attach(display2)

    weather_station.set_temperature(25.0)
    print()
    weather_station.set_temperature(30.0)
    print()
    weather_station.detach(display1)
    weather_station.set_temperature(28.0)
