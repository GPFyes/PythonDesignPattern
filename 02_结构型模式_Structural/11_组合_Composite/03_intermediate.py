from abc import ABC, abstractmethod
from typing import List, Optional

class FileSystemComponent(ABC):
    def __init__(self, name: str):
        self.name = name
        self.parent: Optional['Folder'] = None

    @abstractmethod
    def get_size(self) -> int: pass
    @abstractmethod
    def display(self, indent: int = 0): pass

    def get_path(self) -> str:
        return f"{self.parent.get_path()}/{self.name}" if self.parent else self.name

class File(FileSystemComponent):
    def __init__(self, name: str, size: int):
        super().__init__(name)
        self.size = size

    def get_size(self) -> int: return self.size
    def display(self, indent: int = 0):
        print(" " * indent + f"File: {self.name} ({self.size}KB)")

class Folder(FileSystemComponent):
    def __init__(self, name: str):
        super().__init__(name)
        self.children: List[FileSystemComponent] = []

    def add(self, c: FileSystemComponent) -> None:
        c.parent = self
        self.children.append(c)

    def get_size(self) -> int: return sum(c.get_size() for c in self.children)

    def display(self, indent: int = 0):
        print(" " * indent + f"Folder: {self.name}/ ({self.get_size()}KB)")
        for c in self.children: c.display(indent + 2)

    def find(self, name: str) -> Optional[FileSystemComponent]:
        if self.name == name: return self
        for c in self.children:
            if c.name == name: return c
            if isinstance(c, Folder):
                r = c.find(name)
                if r: return r
        return None

root = Folder("root")
root.add(File("readme.txt", 10))
docs = Folder("documents")
docs.add(File("notes.txt", 20))
root.add(docs)
root.display()
print(f"Total: {root.get_size()}KB")
print(f"Path: {docs.get_path()}")
found = root.find("notes.txt")
print(f"Found: {found.name if found else 'Not found'}")
