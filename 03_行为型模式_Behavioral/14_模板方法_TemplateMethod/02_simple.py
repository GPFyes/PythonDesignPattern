from abc import ABC, abstractmethod
from typing import Any


class DataMiner(ABC):
    def mine(self, file_path: str) -> dict:
        raw_data = self.open_file(file_path)
        data = self.parse_data(raw_data)
        cleaned = self.clean_data(data)
        analysis = self.analyze_data(cleaned)
        report = self.generate_report(analysis)
        self.save_report(report)
        return report

    @abstractmethod
    def open_file(self, file_path: str) -> str:
        pass

    @abstractmethod
    def parse_data(self, raw_data: str) -> list[dict]:
        pass

    def clean_data(self, data: list[dict]) -> list[dict]:
        return [row for row in data if row]

    @abstractmethod
    def analyze_data(self, data: list[dict]) -> dict:
        pass

    @abstractmethod
    def generate_report(self, analysis: dict) -> str:
        pass

    def save_report(self, report: str) -> None:
        print(f"保存报告: {report[:50]}...")


class CSVDataMiner(DataMiner):
    def open_file(self, file_path: str) -> str:
        print(f"打开CSV文件: {file_path}")
        return "name,age,city\nAlice,25,Beijing\nBob,30,Shanghai"

    def parse_data(self, raw_data: str) -> list[dict]:
        lines = raw_data.strip().split("\n")
        headers = lines[0].split(",")
        return [
            dict(zip(headers, line.split(",")))
            for line in lines[1:]
        ]

    def analyze_data(self, data: list[dict]) -> dict:
        return {
            "total_records": len(data),
            "avg_age": sum(int(row["age"]) for row in data) / len(data)
        }

    def generate_report(self, analysis: dict) -> str:
        return f"CSV分析报告 - 记录数: {analysis['total_records']}, 平均年龄: {analysis['avg_age']:.1f}"


class JSONDataMiner(DataMiner):
    def open_file(self, file_path: str) -> str:
        print(f"打开JSON文件: {file_path}")
        return '[{"name": "Alice", "age": 25}, {"name": "Bob", "age": 30}]'

    def parse_data(self, raw_data: str) -> list[dict]:
        import json
        return json.loads(raw_data)

    def analyze_data(self, data: list[dict]) -> dict:
        return {
            "total_records": len(data),
            "avg_age": sum(row["age"] for row in data) / len(data)
        }

    def generate_report(self, analysis: dict) -> str:
        return f"JSON分析报告 - 记录数: {analysis['total_records']}, 平均年龄: {analysis['avg_age']:.1f}"


class XMLDataMiner(DataMiner):
    def open_file(self, file_path: str) -> str:
        print(f"打开XML文件: {file_path}")
        return "<users><user><name>Alice</name><age>25</age></user><user><name>Bob</name><age>30</age></user></users>"

    def parse_data(self, raw_data: str) -> list[dict]:
        import re
        users = re.findall(r"<name>(.*?)</name><age>(.*?)</age>", raw_data)
        return [{"name": name, "age": int(age)} for name, age in users]

    def analyze_data(self, data: list[dict]) -> dict:
        return {
            "total_records": len(data),
            "avg_age": sum(row["age"] for row in data) / len(data)
        }

    def generate_report(self, analysis: dict) -> str:
        return f"XML分析报告 - 记录数: {analysis['total_records']}, 平均年龄: {analysis['avg_age']:.1f}"


if __name__ == "__main__":
    miners = [
        CSVDataMiner(),
        JSONDataMiner(),
        XMLDataMiner()
    ]

    for miner in miners:
        result = miner.mine("data")
        print(f"结果: {result}\n")
