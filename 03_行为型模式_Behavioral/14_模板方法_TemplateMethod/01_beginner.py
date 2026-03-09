from abc import ABC, abstractmethod


class DataMiner(ABC):
    def mine(self, file_path: str) -> str:
        raw_data = self.open_file(file_path)
        data = self.parse_data(raw_data)
        analysis = self.analyze_data(data)
        return self.generate_report(analysis)

    @abstractmethod
    def open_file(self, file_path: str) -> str:
        pass

    @abstractmethod
    def parse_data(self, raw_data: str) -> list:
        pass

    @abstractmethod
    def analyze_data(self, data: list) -> dict:
        pass

    def generate_report(self, analysis: dict) -> str:
        return f"分析结果: {analysis}"


class CSVDataMiner(DataMiner):
    def open_file(self, file_path: str) -> str:
        return f"CSV文件内容: {file_path}"

    def parse_data(self, raw_data: str) -> list:
        return ["row1", "row2", "row3"]

    def analyze_data(self, data: list) -> dict:
        return {"rows": len(data), "type": "CSV"}


class JSONDataMiner(DataMiner):
    def open_file(self, file_path: str) -> str:
        return f"JSON文件内容: {file_path}"

    def parse_data(self, raw_data: str) -> list:
        return [{"key": "value1"}, {"key": "value2"}]

    def analyze_data(self, data: list) -> dict:
        return {"records": len(data), "type": "JSON"}


if __name__ == "__main__":
    csv_miner = CSVDataMiner()
    print(csv_miner.mine("data.csv"))

    json_miner = JSONDataMiner()
    print(json_miner.mine("data.json"))
