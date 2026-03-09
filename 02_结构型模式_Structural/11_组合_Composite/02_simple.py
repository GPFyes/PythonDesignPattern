from abc import ABC, abstractmethod

class FileSystemComponent(ABC):
    def __init__(self, name):
        self.name = name
    @abstractmethod
    def get_size(self) -> int: pass
    @abstractmethod
    def display(self, indent=0): pass

class File(FileSystemComponent):
    def __init__(self, name, size):
        super().__init__(name)
        self.size = size
    def get_size(self) -> int: return self.size
    def display(self, indent=0):
        print(" " * indent + f"File: {self.name} ({self.size}KB)")

class Folder(FileSystemComponent):
    def __init__(self, name):
        super().__init__(name)
        self.children = []
    def add(self, c): self.children.append(c)
    def get_size(self) -> int: return sum(c.get_size() for c in self.children)
    def display(self, indent=0):
        print(" " * indent + f"Folder: {self.name}")
        for c in self.children: c.display(indent + 2)

root = Folder("root")
root.add(File("readme.txt", 10))
docs = Folder("documents")
docs.add(File("notes.txt", 20))
root.add(docs)
root.display()
print(f"Total: {root.get_size()}KB")
