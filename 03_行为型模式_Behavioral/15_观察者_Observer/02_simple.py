from abc import ABC, abstractmethod
from typing import List


class WeatherObserver(ABC):
    @abstractmethod
    def update(self, temperature: float, humidity: float) -> None:
        pass


class WeatherStation:
    def __init__(self) -> None:
        self._observers: List[WeatherObserver] = []
        self._temperature: float = 0.0
        self._humidity: float = 0.0

    def attach(self, observer: WeatherObserver) -> None:
        self._observers.append(observer)

    def detach(self, observer: WeatherObserver) -> None:
        self._observers.remove(observer)

    def notify(self) -> None:
        for observer in self._observers:
            observer.update(self._temperature, self._humidity)

    def set_weather(self, temperature: float, humidity: float) -> None:
        print(f"气象站: 更新天气数据 - 温度 {temperature}°C, 湿度 {humidity}%")
        self._temperature = temperature
        self._humidity = humidity
        self.notify()


class CurrentConditionsDisplay(WeatherObserver):
    def __init__(self, name: str) -> None:
        self.name = name

    def update(self, temperature: float, humidity: float) -> None:
        print(f"[{self.name}] 当前条件: 温度 {temperature}°C, 湿度 {humidity}%")


class StatisticsDisplay(WeatherObserver):
    def __init__(self, name: str) -> None:
        self.name = name
        self.temperatures: List[float] = []

    def update(self, temperature: float, humidity: float) -> None:
        self.temperatures.append(temperature)
        avg = sum(self.temperatures) / len(self.temperatures)
        print(f"[{self.name}] 平均温度: {avg:.1f}°C, 记录数: {len(self.temperatures)}")


class ForecastDisplay(WeatherObserver):
    def __init__(self, name: str) -> None:
        self.name = name
        self.last_temperature: float = 0.0

    def update(self, temperature: float, humidity: float) -> None:
        diff = temperature - self.last_temperature
        if self.last_temperature != 0:
            trend = "上升" if diff > 0 else "下降" if diff < 0 else "持平"
            print(f"[{self.name}] 温度趋势: {trend} {abs(diff):.1f}°C")
        self.last_temperature = temperature


if __name__ == "__main__":
    weather_station = WeatherStation()

    current_display = CurrentConditionsDisplay("当前状况")
    stats_display = StatisticsDisplay("统计数据")
    forecast_display = ForecastDisplay("天气预报")

    weather_station.attach(current_display)
    weather_station.attach(stats_display)
    weather_station.attach(forecast_display)

    weather_station.set_weather(25.0, 60.0)
    print()
    weather_station.set_weather(28.0, 55.0)
    print()
    weather_station.set_weather(22.0, 70.0)
