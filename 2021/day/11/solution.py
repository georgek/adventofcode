from __future__ import annotations

from curtsies.fmtfuncs import bold


class SquareGrid:
    def __init__(self, points: dict[tuple, int], size: int):
        self.points = points
        self.size = size

    @classmethod
    def from_strings(cls, strings: list[str]) -> SquareGrid:
        dimension = len(strings)
        points = {}
        for y, string in enumerate(strings):
            for x, char in enumerate(string):
                points[(x, y)] = int(char)

        return cls(points, dimension)

    def adjacent_points(self, point: tuple[int, int]) -> list[tuple]:
        x, y = point
        return [
            (new_x, new_y)
            for new_x in range(x-1, x+2)
            for new_y in range(y-1, y+2)
            if new_x >= 0
            and new_y >= 0
            and new_x < self.size
            and new_y < self.size
            and (new_x, new_y) != point
        ]

    def tick(self) -> int:
        self.points = {loc: val+1 for loc, val in self.points.items()}
        flashes = {point for point, val in self.points.items() if val > 9}
        new_flashes = set(flashes)
        while new_flashes:
            for flash in new_flashes:
                self.points[flash] = 0
                for adj in set(self.adjacent_points(flash)) - flashes:
                    self.points[adj] += 1
            new_flashes = {point for point, val in self.points.items() if val > 9}
            flashes = flashes.union(new_flashes)

        return flashes

    def __str__(self):
        output = []
        for y in range(self.size):
            output.append("".join(str(self.points[(x, y)]) for x in range(self.size)))
        return "\n".join(output)


with open("test-input") as fin:
    lines = [line.strip() for line in fin.readlines()]

grid = SquareGrid.from_strings(lines)

total_flashes = 0
all_flashed = None
flashes = set()
for t in range(10):
    print(f"After step {t}:")
    if len(flashes) == grid.size**2 and all_flashed is None:
        all_flashed = t
    for y in range(grid.size):
        line = []
        for x in range(grid.size):
            if (x, y) in flashes:
                line.append(bold(str(grid.points[(x, y)])))
            else:
                line.append((str(grid.points[(x, y)])))
        print("".join(str(char) for char in line))
    flashes = grid.tick()
    total_flashes += len(flashes)

print(total_flashes)
print(all_flashed)
