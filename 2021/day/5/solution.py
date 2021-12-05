from __future__ import annotations

from collections import defaultdict


class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    @classmethod
    def from_string(cls, string: str) -> Point:
        x, y = string.split(",")
        return cls(int(x), int(y))

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __repr__(self):
        return f"Point({self.x}, {self.y})"


class Line:
    def __init__(self, point_from: Point, point_to: Point):
        if point_from.x == point_to.x:
            if point_from.y < point_to.y:
                self.point_from, self.point_to = point_from, point_to
            else:
                self.point_from, self.point_to = point_to, point_from
        elif point_from.y == point_to.y:
            if point_from.x < point_to.x:
                self.point_from, self.point_to = point_from, point_to
            else:
                self.point_from, self.point_to = point_to, point_from
        else:
            if point_from.x < point_to.x:
                self.point_from, self.point_to = point_from, point_to
            else:
                self.point_from, self.point_to = point_to, point_from

    def points(self) -> list[Point]:
        if self.point_from.x == self.point_to.x:
            return [
                Point(self.point_from.x, y)
                for y in range(self.point_from.y, self.point_to.y + 1)
            ]
        elif self.point_from.y == self.point_to.y:
            return [
                Point(x, self.point_from.y)
                for x in range(self.point_from.x, self.point_to.x + 1)
            ]
        else:
            x = [x for x in range(self.point_from.x, self.point_to.x + 1)]
            if self.point_from.y < self.point_to.y:
                y = [y for y in range(self.point_from.y, self.point_to.y + 1)]
            else:
                y = list(reversed(
                    [y for y in range(self.point_to.y, self.point_from.y + 1)]
                ))
            return [Point(x, y) for x, y in zip(x, y)]

    @property
    def is_diagonal(self) -> bool:
        return self.point_from.x != self.point_to.x \
            and self.point_from.y != self.point_to.y

    @classmethod
    def from_string(cls, string: str) -> Line:
        point_from, _, point_to = string.split()
        return cls(Point.from_string(point_from), Point.from_string(point_to))

    def __str__(self):
        return f"{self.point_from} -> {self.point_to}"


class Grid:
    def __init__(self):
        self.points = defaultdict(int)
        self.x_limit = 0
        self.y_limit = 0

    def add_line(self, line: Line):
        for point in line.points():
            self.x_limit = max(point.x + 1, self.x_limit)
            self.y_limit = max(point.y + 1, self.y_limit)
            self.points[point] += 1

    def num_deep(self) -> int:
        return len([count for count in self.points.values() if count > 1])

    def __str__(self) -> str:
        lines = []
        for y in range(self.y_limit):
            line = []
            for x in range(self.x_limit):
                line.append(str(self.points[Point(x, y)]))
            lines.append("".join(line))
        return "\n".join(lines)


with open("input") as fin:
    grid = Grid()
    for fin_line in fin:
        line = Line.from_string(fin_line)
        if line.is_diagonal:
            continue
        grid.add_line(line)

print(grid.num_deep())

with open("input") as fin:
    grid = Grid()
    for fin_line in fin:
        line = Line.from_string(fin_line)
        grid.add_line(line)

print(grid.num_deep())
