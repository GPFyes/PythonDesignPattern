from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import datetime

class FileSystemComponent(ABC):
    def __init__(self, name: str):
        self.name = name
        self.created_at = datetime.now()
        self.parent: Optional['Folder'] = None

    @abstractmethod
    def get_size(self) -> int: pass
    @abstractmethod
    def display(self, indent: int = 0) -> str: pass

    def get_path(self) -> str:
        return f"{self.parent.get_path()}/{self.name}" if self.parent else self.name
    def get_created_time(self) -> str:
        return self.created_at.strftime("%Y-%m-%d %H:%M:%S")

class File(FileSystemComponent):
    def __init__(self, name: str, size: int, content: str = ""):
        super().__init__(name)
        self.size = size
        self.content = content

    def get_size(self) -> int: return self.size
    def get_content(self) -> str: return self.content
    def display(self, indent: int = 0) -> str:
        return f"{'  '*indent}File: {self.name} ({self.size}KB)"
    def read(self) -> str: return self.content
    def write(self, content: str) -> None:
        self.content = content
        self.size = len(content)

class Folder(FileSystemComponent):
    def __init__(self, name: str):
        super().__init__(name)
        self.children: List[FileSystemComponent] = []

    def add(self, c: FileSystemComponent) -> None:
        c.parent = self
        self.children.append(c)
    def remove(self, c: FileSystemComponent) -> None:
        if c in self.children:
            c.parent = None
            self.children.remove(c)
    def get_size(self) -> int: return sum(c.get_size() for c in self.children)
    def get_children(self) -> List[FileSystemComponent]: return self.children

    def find_by_name(self, name: str) -> Optional[FileSystemComponent]:
        if self.name == name: return self
        for c in self.children:
            if c.name == name: return c
            if isinstance(c, Folder):
                r = c.find_by_name(name)
                if r: return r
        return None

    def display(self, indent: int = 0) -> str:
        lines = [f"{'  '*indent}Folder: {self.name}/ ({self.get_size()}KB)"]
        for c in self.children: lines.append(c.display(indent + 1))
        return "\n".join(lines)

class FileSystemVisitor(ABC):
    @abstractmethod
    def visit_file(self, file: File) -> None: pass
    @abstractmethod
    def visit_folder(self, folder: Folder) -> None: pass

class SizeCalculatorVisitor(FileSystemVisitor):
    def __init__(self):
        self.total_size = 0
    def visit_file(self, file: File) -> None:
        self.total_size += file.get_size()
    def visit_folder(self, folder: Folder) -> None:
        for c in folder.get_children():
            if isinstance(c, File): self.visit_file(c)
            elif isinstance(c, Folder): self.visit_folder(c)

def calculate_size(component: FileSystemComponent) -> int:
    if isinstance(component, File): return component.get_size()
    elif isinstance(component, Folder):
        v = SizeCalculatorVisitor()
        v.visit_folder(component)
        return v.total_size
    return 0

root = Folder("root")
root.add(File("readme.txt", 10, "Welcome"))
docs = Folder("documents")
docs.add(File("notes.txt", 20, "My notes"))
root.add(docs)
print(root.display())
print(f"Total: {root.get_size()}KB")
found = root.find_by_name("notes.txt")
if found: print(f"Found: {found.get_path()}")
print(f"Documents: {calculate_size(docs)}KB")
