"""
访问者模式 - 中级示例

实现文件系统的访问者操作
"""

from abc import ABC, abstractmethod
from typing import List


class FileSystemItem(ABC):
    @abstractmethod
    def accept(self, visitor: "FileSystemVisitor") -> None:
        pass


class File(FileSystemItem):
    def __init__(self, name: str, size: int):
        self.name = name
        self.size = size

    def accept(self, visitor: "FileSystemVisitor") -> None:
        visitor.visit_file(self)


class Folder(FileSystemItem):
    def __init__(self, name: str):
        self.name = name
        self.children: List[FileSystemItem] = []

    def add(self, item: FileSystemItem) -> None:
        self.children.append(item)

    def accept(self, visitor: "FileSystemVisitor") -> None:
        visitor.visit_folder(self)


class FileSystemVisitor(ABC):
    @abstractmethod
    def visit_file(self, file: File) -> None:
        pass

    @abstractmethod
    def visit_folder(self, folder: Folder) -> None:
        pass


class SizeCalculator(FileSystemVisitor):
    def __init__(self):
        self.total_size = 0
        self.file_count = 0

    def visit_file(self, file: File) -> None:
        self.total_size += file.size
        self.file_count += 1
        print(f"  文件: {file.name} ({file.size} KB)")

    def visit_folder(self, folder: Folder) -> None:
        print(f"文件夹: {folder.name}")
        for child in folder.children:
            child.accept(self)


class FileSearcher(FileSystemVisitor):
    def __init__(self, extension: str):
        self.extension = extension
        self.results: List[File] = []

    def visit_file(self, file: File) -> None:
        if file.name.endswith(self.extension):
            self.results.append(file)

    def visit_folder(self, folder: Folder) -> None:
        for child in folder.children:
            child.accept(self)


class FileLister(FileSystemVisitor):
    def __init__(self, indent: int = 0):
        self.indent = indent

    def visit_file(self, file: File) -> None:
        print(" " * self.indent + f"📄 {file.name}")

    def visit_folder(self, folder: Folder) -> None:
        print(" " * self.indent + f"📁 {folder.name}/")
        for child in folder.children:
            child.accept(FileLister(self.indent + 2))


class FileCopier(FileSystemVisitor):
    def __init__(self, target_folder: Folder):
        self.target_folder = target_folder
        self.copied: List[FileSystemItem] = []

    def visit_file(self, file: File) -> None:
        new_file = File(f"copy_{file.name}", file.size)
        self.target_folder.add(new_file)
        self.copied.append(new_file)

    def visit_folder(self, folder: Folder) -> None:
        new_folder = Folder(f"copy_{folder.name}")
        self.target_folder.add(new_folder)
        for child in folder.children:
            temp_copier = FileCopier(new_folder)
            child.accept(temp_copier)
            self.copied.extend(temp_copier.copied)


def create_demo_structure() -> Folder:
    root = Folder("project")

    src = Folder("src")
    src.add(File("main.py", 50))
    src.add(File("utils.py", 30))

    tests = Folder("tests")
    tests.add(File("test_main.py", 20))
    tests.add(File("test_utils.py", 15))

    docs = Folder("docs")
    docs.add(File("README.md", 10))
    docs.add(File("CHANGELOG.md", 5))

    root.add(src)
    root.add(tests)
    root.add(docs)
    root.add(File("setup.py", 10))

    return root


if __name__ == "__main__":
    print("=== 创建文件结构 ===")
    project = create_demo_structure()

    print("\n=== 列出所有文件 ===")
    project.accept(FileLister())

    print("\n=== 计算文件大小 ===")
    calc = SizeCalculator()
    project.accept(calc)
    print(f"\n总文件数: {calc.file_count}")
    print(f"总大小: {calc.total_size} KB")

    print("\n=== 搜索 .py 文件 ===")
    searcher = FileSearcher(".py")
    project.accept(searcher)
    print("找到的文件:")
    for f in searcher.results:
        print(f"  {f.name}")

    print("\n=== 复制文件 ===")
    backup = Folder("backup")
    copier = FileCopier(backup)
    project.accept(copier)
    print("复制完成!")
    print("备份内容:")
    backup.accept(FileLister())
