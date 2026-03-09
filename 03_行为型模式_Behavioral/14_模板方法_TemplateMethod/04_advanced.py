from abc import ABC, abstractmethod
from typing import Any, Callable
from datetime import datetime
from enum import Enum
import json


class DataFormat(Enum):
    CSV = "csv"
    JSON = "json"
    XML = "xml"
    EXCEL = "excel"
    PARQUET = "parquet"


class DataMiner(ABC):
    def __init__(self):
        self._hooks: dict[str, Callable] = {}
        self._cache: dict[str, Any] = {}
        
    def mine(self, file_path: str, options: dict = None) -> dict:
        options = options or {}
        
        self._before_start(file_path, options)
        
        if self._should_skip(file_path):
            return self._create_empty_report()
        
        raw_data = self._load_data(file_path)
        
        data = self.parse_data(raw_data)
        
        if options.get("clean", True):
            data = self.clean_data(data)
        
        if options.get("validate", True):
            if not self.validate_data(data):
                return self._create_error_report("数据验证失败")
        
        analysis = self.analyze_data(data, options)
        
        report = self.generate_report(analysis, options)
        
        if options.get("cache", False):
            self._cache[file_path] = report
        
        self._after_complete(report)
        
        return report

    def register_hook(self, event: str, callback: Callable) -> None:
        self._hooks[event] = callback

    def _before_start(self, file_path: str, options: dict) -> None:
        if "before_start" in self._hooks:
            self._hooks["before_start"](file_path, options)
        self.log(f"开始处理文件: {file_path}")

    def _should_skip(self, file_path: str) -> bool:
        if file_path in self._cache:
            self.log(f"使用缓存: {file_path}")
            return True
        return False

    def _create_empty_report(self) -> dict:
        return {"status": "skipped", "reason": "cached"}

    def _create_error_report(self, error: str) -> dict:
        return {"status": "error", "message": error}

    def _after_complete(self, report: dict) -> None:
        if "after_complete" in self._hooks:
            self._hooks["after_complete"](report)
        self.log(f"处理完成: {report.get('status')}")

    @abstractmethod
    def _load_data(self, file_path: str) -> str:
        pass

    @abstractmethod
    def parse_data(self, raw_data: str) -> list[dict]:
        pass

    def clean_data(self, data: list[dict]) -> list[dict]:
        return [row for row in data if row and all(row.values())]

    def validate_data(self, data: list[dict]) -> bool:
        return len(data) > 0

    @abstractmethod
    def analyze_data(self, data: list[dict], options: dict) -> dict:
        pass

    @abstractmethod
    def generate_report(self, analysis: dict, options: dict) -> dict:
        pass

    def log(self, message: str) -> None:
        print(f"[{self.__class__.__name__}] {message}")


class CSVDataMiner(DataMiner):
    def _load_data(self, file_path: str) -> str:
        return "name,age,city,salary,department\nAlice,25,Beijing,15000,IT\nBob,30,Shanghai,20000,HR\nCarol,28,Shenzhen,18000,IT\nDavid,35,Beijing,25000,Sales"

    def parse_data(self, raw_data: str) -> list[dict]:
        lines = raw_data.strip().split("\n")
        headers = lines[0].split(",")
        return [
            dict(zip(headers, line.split(",")))
            for line in lines[1:]
        ]

    def analyze_data(self, data: list[dict], options: dict) -> dict:
        numeric_fields = options.get("numeric_fields", ["age", "salary"])
        
        analysis = {
            "total_records": len(data),
            "fields": list(data[0].keys()) if data else []
        }
        
        for field in numeric_fields:
            if field in (data[0] if data else {}):
                values = [int(row[field]) for row in data]
                analysis[f"stats_{field}"] = {
                    "min": min(values),
                    "max": max(values),
                    "avg": sum(values) / len(values),
                    "sum": sum(values)
                }
        
        categorical_fields = [k for k in (data[0] if data else {}).keys() if k not in numeric_fields]
        for field in categorical_fields:
            if field in (data[0] if data else {}):
                counts: dict = {}
                for row in data:
                    key = row[field]
                    counts[key] = counts.get(key, 0) + 1
                analysis[f"counts_{field}"] = counts
        
        return analysis

    def generate_report(self, analysis: dict, options: dict) -> dict:
        format_type = options.get("format", "summary")
        
        report = {
            "status": "success",
            "format": "CSV",
            "timestamp": datetime.now().isoformat(),
            "analysis": analysis
        }
        
        if format_type == "detailed":
            report["metadata"] = {
                "miner": self.__class__.__name__,
                "version": "1.0"
            }
        
        return report


class JSONDataMiner(DataMiner):
    def _load_data(self, file_path: str) -> str:
        return json.dumps([
            {"name": "Alice", "age": 25, "city": "Beijing", "salary": 15000, "skills": ["Python", "Java"]},
            {"name": "Bob", "age": 30, "city": "Shanghai", "salary": 20000, "skills": ["JavaScript", "Python"]},
            {"name": "Carol", "age": 28, "city": "Shenzhen", "salary": 18000, "skills": ["Go", "Python"]}
        ])

    def parse_data(self, raw_data: str) -> list[dict]:
        return json.loads(raw_data)

    def analyze_data(self, data: list[dict], options: dict) -> dict:
        numeric_fields = ["age", "salary"]
        
        analysis: dict = {
            "total_records": len(data),
            "fields": list(data[0].keys()) if data else []
        }
        
        for field in numeric_fields:
            if field in (data[0] if data else {}):
                values = [int(row[field]) for row in data]
                analysis[f"stats_{field}"] = {
                    "min": min(values),
                    "max": max(values),
                    "avg": sum(values) / len(values),
                    "sum": sum(values)
                }
        
        if "skills" in (data[0] if data else {}):
            all_skills = []
            for row in data:
                all_skills.extend(row.get("skills", []))
            skill_counts: dict = {}
            for skill in all_skills:
                skill_counts[skill] = skill_counts.get(skill, 0) + 1
            analysis["skills_distribution"] = skill_counts
        
        return analysis

    def generate_report(self, analysis: dict, options: dict) -> dict:
        format_type = options.get("format", "summary")
        
        report = {
            "status": "success",
            "format": "JSON",
            "timestamp": datetime.now().isoformat(),
            "analysis": analysis
        }
        
        if format_type == "detailed":
            report["metadata"] = {
                "miner": self.__class__.__name__,
                "version": "1.0"
            }
        
        return report


class DataMinerFactory:
    _miners: dict[DataFormat, type[DataMiner]] = {}
    
    @classmethod
    def register(cls, format_type: DataFormat, miner_class: type[DataMiner]) -> None:
        cls._miners[format_type] = miner_class
    
    @classmethod
    def create(cls, format_type: DataFormat) -> DataMiner:
        if format_type not in cls._miners:
            raise ValueError(f"未支持的格式: {format_type}")
        return cls._miners[format_type]()
    
    @classmethod
    def get_supported_formats(cls) -> list[DataFormat]:
        return list(cls._miners.keys())


DataMinerFactory.register(DataFormat.CSV, CSVDataMiner)
DataMinerFactory.register(DataFormat.JSON, JSONDataMiner)


def main():
    print("=" * 60)
    print("模板方法模式 - 数据挖掘框架")
    print("=" * 60)
    
    miner = DataMinerFactory.create(DataFormat.CSV)
    
    miner.register_hook("before_start", lambda f, o: print(f"  [Hook] 即将处理: {f}"))
    miner.register_hook("after_complete", lambda r: print(f"  [Hook] 报告状态: {r.get('status')}"))
    
    options = {
        "clean": True,
        "validate": True,
        "numeric_fields": ["age", "salary"],
        "format": "detailed"
    }
    
    print("\n--- CSV 数据挖掘 ---")
    report = miner.mine("employees.csv", options)
    print(f"\n最终报告:\n{json.dumps(report, indent=2, ensure_ascii=False)}")
    
    print("\n" + "=" * 60)
    
    json_miner = DataMinerFactory.create(DataFormat.JSON)
    print("\n--- JSON 数据挖掘 ---")
    report = json_miner.mine("employees.json", options)
    print(f"\n最终报告:\n{json.dumps(report, indent=2, ensure_ascii=False)}")


if __name__ == "__main__":
    main()
