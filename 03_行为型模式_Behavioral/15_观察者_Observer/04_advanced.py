from abc import ABC, abstractmethod
from typing import List, Dict, Any, Callable, Optional
from datetime import datetime
import time
import random


class Observer(ABC):
    @abstractmethod
    def update(self, data: Dict[str, Any]) -> None:
        pass

    @abstractmethod
    def get_name(self) -> str:
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


class Observable:
    def __init__(self) -> None:
        self._observers: List[Observer] = []
        self._changed: bool = False

    def attach(self, observer: Observer) -> None:
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        if observer in self._observers:
            self._observers.remove(observer)

    def notify_observers(self, data: Dict[str, Any]) -> None:
        for observer in self._observers:
            observer.update(data)

    def set_changed(self) -> None:
        self._changed = True

    def clear_changed(self) -> None:
        self._changed = False

    def has_changed(self) -> bool:
        return self._changed


class WeatherStation(Observable):
    def __init__(self, name: str) -> None:
        super().__init__()
        self.name = name
        self._data: Dict[str, Any] = {}
        self._history: List[Dict[str, Any]] = []

    def set_measurements(self, temperature: float, humidity: float, 
                        pressure: float, wind_speed: float = 0.0) -> None:
        self._data = {
            "temperature": temperature,
            "humidity": humidity,
            "pressure": pressure,
            "wind_speed": wind_speed,
            "timestamp": datetime.now()
        }
        self._history.append(self._data.copy())
        self.set_changed()
        self.notify_observers(self._data)

    def get_current_data(self) -> Dict[str, Any]:
        return self._data.copy()

    def get_history(self) -> List[Dict[str, Any]]:
        return self._history.copy()


class CurrentConditionsDisplay(Observer):
    def __init__(self, name: str) -> None:
        self.name = name

    def update(self, data: Dict[str, Any]) -> None:
        print(f"[{self.name}] {data.get('timestamp', 'N/A')}")
        print(f"  温度: {data.get('temperature', 0):.1f}°C")
        print(f"  湿度: {data.get('humidity', 0):.1f}%")
        print(f"  气压: {data.get('pressure', 0):.0f}hPa")
        print(f"  风速: {data.get('wind_speed', 0):.1f}m/s")

    def get_name(self) -> str:
        return self.name


class StatisticsDisplay(Observer):
    def __init__(self, name: str) -> None:
        self.name = name
        self.temps: List[float] = []
        self.humidities: List[float] = []
        self.pressures: List[float] = []

    def update(self, data: Dict[str, Any]) -> None:
        self.temps.append(data.get("temperature", 0))
        self.humidities.append(data.get("humidity", 0))
        self.pressures.append(data.get("pressure", 0))

        print(f"[{self.name}] 统计 ({len(self.temps)} 次记录)")
        print(f"  温度 - 平均: {sum(self.temps)/len(self.temps):.1f}°C, "
              f"最高: {max(self.temps):.1f}°C, 最低: {min(self.temps):.1f}°C")
        print(f"  湿度 - 平均: {sum(self.humidities)/len(self.humidities):.1f}%")
        print(f"  气压 - 平均: {sum(self.pressures)/len(self.pressures):.0f}hPa")

    def get_name(self) -> str:
        return self.name


class ForecastDisplay(Observer):
    def __init__(self, name: str) -> None:
        self.name = name
        self.last_data: Optional[Dict[str, Any]] = None

    def update(self, data: Dict[str, Any]) -> None:
        if self.last_data:
            temp_diff = data.get("temperature", 0) - self.last_data.get("temperature", 0)
            hum_diff = data.get("humidity", 0) - self.last_data.get("humidity", 0)
            pres_diff = data.get("pressure", 0) - self.last_data.get("pressure", 0)

            print(f"[{self.name}] 变化趋势")
            temp_trend = "↑" if temp_diff > 0 else "↓" if temp_diff < 0 else "→"
            hum_trend = "↑" if hum_diff > 0 else "↓" if hum_diff < 0 else "→"
            pres_trend = "↑" if pres_diff > 0 else "↓" if pres_diff < 0 else "→"
            
            print(f"  温度: {temp_trend} {abs(temp_diff):.1f}°C")
            print(f"  湿度: {hum_trend} {abs(hum_diff):.1f}%")
            print(f"  气压: {pres_trend} {abs(pres_diff):.0f}hPa")

            if data.get("temperature", 0) > 35:
                print("  警告: 高温预警!")
            elif data.get("temperature", 0) < 0:
                print("  警告: 低温预警!")
            if data.get("humidity", 0) > 80:
                print("  警告: 湿度较高!")
            if data.get("pressure", 0) < 1000:
                print("  警告: 低气压，可能有风暴!")

        self.last_data = data.copy()

    def get_name(self) -> str:
        return self.name


class AlertDisplay(Observer):
    def __init__(self, name: str, temp_threshold: float = 30.0) -> None:
        self.name = name
        self.temp_threshold = temp_threshold

    def update(self, data: Dict[str, Any]) -> None:
        temp = data.get("temperature", 0)
        humidity = data.get("humidity", 0)
        wind_speed = data.get("wind_speed", 0)

        alerts = []

        if temp > self.temp_threshold:
            alerts.append(f"高温警告: {temp:.1f}°C")
        if temp < 0:
            alerts.append(f"低温警告: {temp:.1f}°C")
        if humidity > 85:
            alerts.append(f"高湿度警告: {humidity:.1f}%")
        if wind_speed > 20:
            alerts.append(f"大风警告: {wind_speed:.1f}m/s")

        if alerts:
            print(f"[{self.name}] 警报!")
            for alert in alerts:
                print(f"  ⚠ {alert}")

    def get_name(self) -> str:
        return self.name


class WeatherStationFacade:
    def __init__(self, station_name: str):
        self._station = WeatherStation(station_name)
        self._displays: List[Observer] = []

    def add_display(self, display: Observer) -> None:
        self._displays.append(display)
        self._station.attach(display)

    def remove_display(self, display: Observer) -> None:
        if display in self._displays:
            self._displays.remove(display)
            self._station.detach(display)

    def update_weather(self, temperature: float, humidity: float,
                       pressure: float, wind_speed: float = 0.0) -> None:
        self._station.set_measurements(temperature, humidity, pressure, wind_speed)

    def get_history(self) -> List[Dict[str, Any]]:
        return self._station.get_history()


class WeatherSimulator:
    def __init__(self, facade: WeatherStationFacade):
        self.facade = facade
        self.base_temp = 25.0
        self.base_hum = 60.0
        self.base_pres = 1013.0

    def simulate(self, iterations: int = 5) -> None:
        print("=" * 50)
        print("开始模拟气象数据...")
        print("=" * 50)
        
        for i in range(iterations):
            temp = self.base_temp + random.uniform(-5, 5)
            hum = max(0, min(100, self.base_hum + random.uniform(-15, 15)))
            pres = self.base_pres + random.uniform(-10, 10)
            wind = random.uniform(0, 25)
            
            print(f"\n--- 第 {i+1} 次测量 ---")
            self.facade.update_weather(temp, hum, pres, wind)
            
            self.base_temp = temp
            self.base_hum = hum
            self.base_pres = pres
            
            time.sleep(0.5)


if __name__ == "__main__":
    facade = WeatherStationFacade("北京气象站")

    current_display = CurrentConditionsDisplay("当前显示")
    stats_display = StatisticsDisplay("统计数据")
    forecast_display = ForecastDisplay("预测显示")
    alert_display = AlertDisplay("警报", temp_threshold=32.0)

    facade.add_display(current_display)
    facade.add_display(stats_display)
    facade.add_display(forecast_display)
    facade.add_display(alert_display)

    facade.update_weather(25.0, 60.0, 1013.0, 5.0)
    print()
    facade.update_weather(28.5, 55.0, 1010.0, 10.0)
    print()
    facade.update_weather(33.0, 70.0, 1008.0, 15.0)
    print()
    facade.update_weather(30.0, 85.0, 1005.0, 25.0)

    print("\n" + "=" * 50)
    print("使用模拟器进行连续观测:")
    print("=" * 50)
    simulator = WeatherSimulator(facade)
    simulator.simulate(3)

    print("\n观测历史记录:")
    for record in facade.get_history():
        print(f"  {record.get('timestamp')}: {record.get('temperature'):.1f}°C, "
              f"{record.get('humidity'):.1f}%, {record.get('pressure'):.0f}hPa")
