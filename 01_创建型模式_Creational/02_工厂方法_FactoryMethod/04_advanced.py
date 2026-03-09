"""
工厂方法模式 - 高级示例

简介：生产级实现，展示物流系统中的应用
"""

from abc import ABC, abstractmethod
from typing import List
from datetime import datetime


class Transport(ABC):
    """
    运输工具抽象类（产品角色）
    
    定义运输工具的统一接口
    """
    
    @abstractmethod
    def deliver(self, destination: str, weight: float) -> dict:
        """
        运输货物到目的地
        
        Args:
            destination: 目的地
            weight: 货物重量（公斤）
        
        Returns:
            运输结果字典
        """
        pass
    
    @abstractmethod
    def get_transport_type(self) -> str:
        """获取运输工具类型"""
        pass
    
    @abstractmethod
    def get_cost_per_km(self) -> float:
        """获取每公里成本"""
        pass


class Truck(Transport):
    """卡车运输"""
    
    def __init__(self, license_plate: str = "京A12345"):
        self.license_plate = license_plate
        self.capacity = 5000  # 载重5吨
    
    def deliver(self, destination: str, weight: float) -> dict:
        if weight > self.capacity:
            raise ValueError(f"超过卡车载重能力 {self.capacity}kg")
        
        distance = 500  # 假设距离500公里
        cost = distance * self.get_cost_per_km()
        
        return {
            "type": self.get_transport_type(),
            "plate": self.license_plate,
            "destination": destination,
            "weight": weight,
            "distance": distance,
            "cost": cost,
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def get_transport_type(self) -> str:
        return "卡车运输"
    
    def get_cost_per_km(self) -> float:
        return 2.0  # 每公里2元


class Ship(Transport):
    """轮船运输"""
    
    def __init__(self, name: str = "海运号"):
        self.name = name
        self.capacity = 100000  # 载重100吨
    
    def deliver(self, destination: str, weight: float) -> dict:
        if weight > self.capacity:
            raise ValueError(f"超过轮船载重能力 {self.capacity}kg")
        
        distance = 2000  # 假设距离2000公里
        cost = distance * self.get_cost_per_km()
        
        return {
            "type": self.get_transport_type(),
            "ship": self.name,
            "destination": destination,
            "weight": weight,
            "distance": distance,
            "cost": cost,
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def get_transport_type(self) -> str:
        return "海运"
    
    def get_cost_per_km(self) -> float:
        return 0.5  # 每公里0.5元


class Airplane(Transport):
    """飞机运输"""
    
    def __init__(self, flight_number: str = "CA1234"):
        self.flight_number = flight_number
        self.capacity = 50000  # 载重50吨
    
    def deliver(self, destination: str, weight: float) -> dict:
        if weight > self.capacity:
            raise ValueError(f"超过飞机载重能力 {self.capacity}kg")
        
        distance = 1500  # 假设距离1500公里
        cost = distance * self.get_cost_per_km()
        
        return {
            "type": self.get_transport_type(),
            "flight": self.flight_number,
            "destination": destination,
            "weight": weight,
            "distance": distance,
            "cost": cost,
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def get_transport_type(self) -> str:
        return "航空运输"
    
    def get_cost_per_km(self) -> float:
        return 5.0  # 每公里5元


class LogisticsFactory(ABC):
    """
    物流工厂抽象类（创建者角色）
    
    声明创建运输工具的工厂方法
    """
    
    @abstractmethod
    def create_transport(self) -> Transport:
        """创建运输工具的工厂方法"""
        pass
    
    @abstractmethod
    def get_company_name(self) -> str:
        """获取公司名称"""
        pass


class RoadLogisticsFactory(LogisticsFactory):
    """公路物流工厂"""
    
    def create_transport(self) -> Transport:
        return Truck()
    
    def get_company_name(self) -> str:
        return "公路物流公司"


class SeaLogisticsFactory(LogisticsFactory):
    """海运物流工厂"""
    
    def create_transport(self) -> Transport:
        return Ship()
    
    def get_company_name(self) -> str:
        return "海运物流公司"


class AirLogisticsFactory(LogisticsFactory):
    """航空物流工厂"""
    
    def create_transport(self) -> Transport:
        return Airplane()
    
    def get_company_name(self) -> str:
        return "航空物流公司"


class Logistics:
    """
    物流系统（客户端）
    
    使用工厂方法创建运输工具
    """
    
    def __init__(self, factory: LogisticsFactory):
        """初始化物流系统，传入工厂"""
        self.factory = factory
        self.transport = factory.create_transport()
    
    def plan_delivery(self, destination: str, weight: float) -> dict:
        """
        计划配送
        
        Args:
            destination: 目的地
            weight: 货物重量
        
        Returns:
            配送信息
        """
        print(f"\n{self.factory.get_company_name()} 计划配送")
        print(f"运输工具: {self.transport.get_transport_type()}")
        
        try:
            result = self.transport.deliver(destination, weight)
            print(f"配送成功！费用: {result['cost']:.2f} 元")
            return result
        except ValueError as e:
            print(f"配送失败: {e}")
            return {"error": str(e)}


def main():
    """测试工厂方法模式 - 物流系统"""
    print("=" * 60)
    print("工厂方法模式 - 物流系统")
    print("=" * 60)
    
    # 公路物流
    road_logistics = Logistics(RoadLogisticsFactory())
    result1 = road_logistics.plan_delivery("北京", 1000)
    
    # 海运物流
    sea_logistics = Logistics(SeaLogisticsFactory())
    result2 = sea_logistics.plan_delivery("上海", 50000)
    
    # 航空物流
    air_logistics = Logistics(AirLogisticsFactory())
    result3 = air_logistics.plan_delivery("广州", 10000)
    
    print("\n" + "=" * 60)
    print("说明：")
    print("- 不同物流公司使用不同的运输工具")
    print("- 新增运输方式只需添加新的工厂和产品类")
    print("- 符合开闭原则，便于扩展")
    print("=" * 60)


if __name__ == "__main__":
    main()
