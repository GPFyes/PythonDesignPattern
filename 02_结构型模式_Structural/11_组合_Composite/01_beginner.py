class File:
    def __init__(self, n, s): self.n, self.s = n, s
    def get_size(self): return self.s

class Folder:
    def __init__(self, n): self.n, self.c = n, []
    def add(self, i): self.c.append(i)
    def get_size(self): return sum(x.get_size() for x in self.c)

f = Folder("root")
f.add(File("a.txt", 100))
f.add(File("b.txt", 200))
s = Folder("sub")
s.add(File("c.txt", 50))
f.add(s)
print(f"Total: {f.get_size()}")
