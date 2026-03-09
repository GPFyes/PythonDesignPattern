from abc import ABC, abstractmethod
from typing import Any
from datetime import datetime


class DataMiner(ABC):
    def mine(self, file_path: str) -> dict:
        self.log(f"开始挖掘: {file_path}")
        
        start = datetime.now()
        raw_data = self.open_file(file_path)
        self.log(f"文件已打开, 大小: {len(raw_data)} 字节")
        
        data = self.parse_data(raw_data)
        self.log(f"解析完成, 共 {len(data)} 条记录")
        
        cleaned = self.clean_data(data)
        self.log(f"清洗完成, 保留 {len(cleaned)} 条记录")
        
        analysis = self.analyze_data(cleaned)
        self.log(f"分析完成")
        
        report = self.generate_report(analysis)
        self.log(f"报告已生成")
        
        self.save_report(report)
        
        elapsed = (datetime.now() - start).total_seconds()
        self.log(f"处理完成, 耗时: {elapsed:.2f}秒")
        
        return report

    def log(self, message: str) -> None:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {message}")

    @abstractmethod
    def open_file(self, file_path: str) -> str:
        pass

    @abstractmethod
    def parse_data(self, raw_data: str) -> list[dict]:
        pass

    def clean_data(self, data: list[dict]) -> list[dict]:
        cleaned = []
        for row in data:
            if row and all(row.values()):
                cleaned.append(row)
        return cleaned

    @abstractmethod
    def analyze_data(self, data: list[dict]) -> dict:
        pass

    @abstractmethod
    def generate_report(self, analysis: dict) -> dict:
        pass

    def save_report(self, report: dict) -> None:
        print(f"保存报告到: reports/{report['timestamp']}.json")


class CSVDataMiner(DataMiner):
    def open_file(self, file_path: str) -> str:
        return "name,age,city,salary\nAlice,25,Beijing,15000\nBob,30,Shanghai,20000\nCarol,28,Shenzhen,18000"

    def parse_data(self, raw_data: str) -> list[dict]:
        lines = raw_data.strip().split("\n")
        headers = lines[0].split(",")
        return [
            dict(zip(headers, line.split(",")))
            for line in lines[1:]
        ]

    def analyze_data(self, data: list[dict]) -> dict:
        ages = [int(row["age"]) for row in data]
        salaries = [int(row["salary"]) for row in data]
        cities = set(row["city"] for row in data)
        
        return {
            "total_records": len(data),
            "avg_age": sum(ages) / len(ages),
            "avg_salary": sum(salaries) / len(salaries),
            "max_salary": max(salaries),
            "min_salary": min(salaries),
            "cities": list(cities)
        }

    def generate_report(self, analysis: dict) -> dict:
        return {
            "type": "CSV",
            "timestamp": datetime.now().isoformat(),
            "analysis": analysis
        }


class JSONDataMiner(DataMiner):
    def open_file(self, file_path: str) -> str:
        return '[{"name": "Alice", "age": 25, "city": "Beijing", "salary": 15000}, {"name": "Bob", "age": 30, "city": "Shanghai", "salary": 20000}]'

    def parse_data(self, raw_data: str) -> list[dict]:
        import json
        return json.loads(raw_data)

    def analyze_data(self, data: list[dict]) -> dict:
        ages = [row["age"] for row in data]
        salaries = [row["salary"] for row in data]
        cities = set(row["city"] for row in data)
        
        return {
            "total_records": len(data),
            "avg_age": sum(ages) / len(ages),
            "avg_salary": sum(salaries) / len(salaries),
            "max_salary": max(salaries),
            "min_salary": min(salaries),
            "cities": list(cities)
        }

    def generate_report(self, analysis: dict) -> dict:
        return {
            "type": "JSON",
            "timestamp": datetime.now().isoformat(),
            "analysis": analysis
        }


class XMLDataMiner(DataMiner):
    def open_file(self, file_path: str) -> str:
        return """<users>
            <user><name>Alice</name><age>25</age><city>Beijing</city><salary>15000</salary></user>
            <user><name>Bob</name><age>30</age><city>Shanghai</city><salary>20000</salary></user>
        </users>"""

    def parse_data(self, raw_data: str) -> list[dict]:
        import re
        users = re.findall(r"<name>(.*?)</name><age>(.*?)</age><city>(.*?)</city><salary>(.*?)</salary>", raw_data)
        return [
            {"name": name, "age": int(age), "city": city, "salary": int(salary)}
            for name, age, city, salary in users
        ]

    def analyze_data(self, data: list[dict]) -> dict:
        ages = [row["age"] for row in data]
        salaries = [row["salary"] for row in data]
        cities = set(row["city"] for row in data)
        
        return {
            "total_records": len(data),
            "avg_age": sum(ages) / len(ages),
            "avg_salary": sum(salaries) / len(salaries),
            "max_salary": max(salaries),
            "min_salary": min(salaries),
            "cities": list(cities)
        }

    def generate_report(self, analysis: dict) -> dict:
        return {
            "type": "XML",
            "timestamp": datetime.now().isoformat(),
            "analysis": analysis
        }


class ExcelDataMiner(DataMiner):
    def open_file(self, file_path: str) -> str:
        return "Name: Alice, Age: 25, City: Beijing, Salary: 15000 | Name: Bob, Age: 30, City: Shanghai, Salary: 20000"

    def parse_data(self, raw_data: str) -> list[dict]:
        records = raw_data.split(" | ")
        data = []
        for record in records:
            parts = record.split(", ")
            row = {}
            for part in parts:
                key, value = part.split(": ", 1)
                if key == "Age" or key == "Salary":
                    row[key.lower()] = int(value)
                else:
                    row[key.lower()] = value
            data.append(row)
        return data

    def analyze_data(self, data: list[dict]) -> dict:
        ages = [row["age"] for row in data]
        salaries = [row["salary"] for row in data]
        cities = set(row["city"] for row in data)
        
        return {
            "total_records": len(data),
            "avg_age": sum(ages) / len(ages),
            "avg_salary": sum(salaries) / len(salaries),
            "max_salary": max(salaries),
            "min_salary": min(salaries),
            "cities": list(cities)
        }

    def generate_report(self, analysis: dict) -> dict:
        return {
            "type": "Excel",
            "timestamp": datetime.now().isoformat(),
            "analysis": analysis
        }


if __name__ == "__main__":
    miners: list[DataMiner] = [
        CSVDataMiner(),
        JSONDataMiner(),
        XMLDataMiner(),
        ExcelDataMiner()
    ]

    for miner in miners:
        print("=" * 50)
        miner.mine("data")
        print()
