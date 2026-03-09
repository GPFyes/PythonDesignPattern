from abc import ABC, abstractmethod
from typing import List, Dict, Any
from datetime import datetime


class Observer(ABC):
    @abstractmethod
    def update(self, subject) -> None:
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


class WeatherData(Subject):
    def __init__(self) -> None:
        self._observers: List[Observer] = []
        self._data: Dict[str, Any] = {}

    def attach(self, observer: Observer) -> None:
        self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        self._observers.remove(observer)

    def notify(self) -> None:
        for observer in self._observers:
            observer.update(self)

    def get_temperature(self) -> float:
        return self._data.get("temperature", 0.0)

    def get_humidity(self) -> float:
        return self._data.get("humidity", 0.0)

    def get_pressure(self) -> float:
        return self._data.get("pressure", 0.0)

    def set_measurements(self, temperature: float, humidity: float, pressure: float) -> None:
        self._data = {
            "temperature": temperature,
            "humidity": humidity,
            "pressure": pressure,
            "timestamp": datetime.now()
        }
        print(f"气象站: 更新数据 - 温度 {temperature}°C, 湿度 {humidity}%, 气压 {pressure}hPa")
        self.notify()


class CurrentConditions(Observer):
    def __init__(self, name: str) -> None:
        self.name = name

    def update(self, subject: WeatherData) -> None:
        print(f"[{self.name}] 温度: {subject.get_temperature()}°C, "
              f"湿度: {subject.get_humidity()}%, 气压: {subject.get_pressure()}hPa")


class Statistics(Observer):
    def __init__(self, name: str) -> None:
        self.name = name
        self.temps: List[float] = []
        self.humidities: List[float] = []

    def update(self, subject: WeatherData) -> None:
        self.temps.append(subject.get_temperature())
        self.humidities.append(subject.get_humidity())
        avg_temp = sum(self.temps) / len(self.temps)
        avg_hum = sum(self.humidities) / len(self.humidities)
        max_temp = max(self.temps)
        min_temp = min(self.temps)
        print(f"[{self.name}] 平均: {avg_temp:.1f}°C/{avg_hum:.1f}%, "
              f"最高: {max_temp}°C, 最低: {min_temp}°C")


class Forecast(Observer):
    def __init__(self, name: str) -> None:
        self.name = name
        self.last_temp = 0.0
        self.last_hum = 0.0

    def update(self, subject: WeatherData) -> None:
        temp_change = subject.get_temperature() - self.last_temp
        hum_change = subject.get_humidity() - self.last_hum
        
        if self.last_temp != 0:
            temp_trend = "↑" if temp_change > 0 else "↓" if temp_change < 0 else "→"
            hum_trend = "↑" if hum_change > 0 else "↓" if hum_change < 0 else "→"
            
            if temp_change > 2:
                prediction = "温度将显著上升"
            elif temp_change < -2:
                prediction = "温度将显著下降"
            else:
                prediction = "温度变化平稳"
            
            print(f"[{self.name}] 温度趋势: {temp_trend} ({temp_change:+.1f}°C) - {prediction}")
            print(f"[{self.name}] 湿度趋势: {hum_trend} ({hum_change:+.1f}%)")
        
        self.last_temp = subject.get_temperature()
        self.last_hum = subject.get_humidity()


class HeatIndex(Observer):
    def __init__(self, name: str) -> None:
        self.name = name

    def update(self, subject: WeatherData) -> None:
        temp = subject.get_temperature()
        hum = subject.get_humidity()
        heat_index = self._calculate_heat_index(temp, hum)
        print(f"[{self.name}] 体感温度: {heat_index:.1f}°C")

    def _calculate_heat_index(self, temperature: float, humidity: float) -> float:
        T = temperature
        R = humidity
        HI = -8.78469475556 + 1.61139411 * T + 2.33854883889 * R
        HI += -0.00114633 * T * R + -0.012616094 * T**2 + -0.0164248277778 * R**2
        HI += 0.002211732 * T**2 * R + 0.00072546 * T * R**2 + -0.000003582 * T**2 * R**2
        return HI


if __name__ == "__main__":
    weather_data = WeatherData()

    current = CurrentConditions("当前显示")
    stats = Statistics("统计数据")
    forecast = Forecast("天气预报")
    heat_index = HeatIndex("体感温度")

    weather_data.attach(current)
    weather_data.attach(stats)
    weather_data.attach(forecast)
    weather_data.attach(heat_index)

    weather_data.set_measurements(25.0, 60.0, 1013.0)
    print()
    weather_data.set_measurements(28.0, 55.0, 1012.0)
    print()
    weather_data.set_measurements(22.0, 70.0, 1010.0)
