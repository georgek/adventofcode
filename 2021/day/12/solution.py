from collections import Counter


class Cave:
    def __init__(self, name: str, is_big: bool):
        self.name = name
        self.is_big = is_big

    @classmethod
    def fromstring(cls, string: str):
        return cls(string, string.isupper())

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.name == other.name

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Cave({self.name!r}, {self.is_big!r})"


class Edge:
    def __init__(self, a: Cave, b: Cave):
        self.a = a
        self.b = b

    def __str__(self):
        return f"{self.a}-{self.b}"

    def __repr__(self):
        return f"Edge({self.a!r}, {self.b!r})"


class Map:
    def __init__(self, caves: set[Cave], edges: set[Edge]):
        self.caves = caves
        self.edges = edges

    def add_edge_from_string(self, string: str):
        name_a, name_b = string.split("-")
        a, b = Cave.fromstring(name_a), Cave.fromstring(name_b)
        edge = Edge(a, b)
        self.caves.add(a)
        self.caves.add(b)
        self.edges.add(edge)

    def siblings(self, cave: Cave) -> set[Cave]:
        siblings = set()
        for edge in self.edges:
            if edge.a == cave:
                siblings.add(edge.b)
            elif edge.b == cave:
                siblings.add(edge.a)

        return siblings

    def all_paths(self) -> list[list[Cave]]:
        paths = []
        start = Cave("start", is_big=False)
        end = Cave("end", is_big=False)

        def extend_path(path: list[Cave]):
            last_cave = path[-1]
            siblings = {
                cave for cave in self.siblings(last_cave)
                if cave.is_big or cave not in path
            }
            if end in siblings:
                paths.append(path + [end])
                siblings.remove(end)

            for sibling in siblings:
                extend_path(path + [sibling])

        extend_path([start])

        return paths

    def all_paths2(self) -> list[list[Cave]]:
        paths = []
        start = Cave("start", is_big=False)
        end = Cave("end", is_big=False)

        def extend_path(path: list[Cave]):
            small_caves_count = Counter(
                cave for cave in path if not cave.is_big
            )
            can_revisit = small_caves_count.most_common()[0][1] < 2
            last_cave = path[-1]
            siblings = {
                cave for cave in self.siblings(last_cave)
                if cave.is_big or cave not in path or can_revisit
            }
            if start in siblings:
                siblings.remove(start)
            if end in siblings:
                paths.append(path + [end])
                siblings.remove(end)

            for sibling in siblings:
                extend_path(path + [sibling])

        extend_path([start])

        return paths

    def __str__(self):
        return f"{self.caves}, {self.edges}"


with open("input") as fin:
    lines = [line.strip() for line in fin.readlines()]

m = Map(set(), set())
for line in lines:
    m.add_edge_from_string(line)

print(m)
paths = m.all_paths()
for path in paths:
    print(",".join(cave.name for cave in path))
print(len(paths))

paths = m.all_paths2()
for path in paths:
    print(",".join(cave.name for cave in path))
print(len(paths))
