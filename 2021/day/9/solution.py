from __future__ import annotations


class DepthMap:
    def __init__(self, points: dict[tuple, int], dimensions: tuple[int, int]):
        self.points = points
        self.x_limit, self.y_limit = dimensions

    @classmethod
    def from_strings(cls, strings: list[str]) -> DepthMap:
        y_limit = len(strings)
        points = {}
        for y, string in enumerate(strings):
            x_limit = len(string)
            for x, char in enumerate(string):
                points[(x, y)] = int(char)

        return cls(points, (x_limit, y_limit))

    def adjacent_points(self, point: tuple[int, int]) -> list[tuple]:
        x, y = point
        adjacent = []
        if x > 0:
            adjacent.append((x-1, y))
        if x < self.x_limit - 1:
            adjacent.append((x+1, y))
        if y > 0:
            adjacent.append((x, y-1))
        if y < self.y_limit - 1:
            adjacent.append((x, y+1))

        return adjacent

    def adjacent_depths(self, point: tuple[int, int]) -> list[int]:
        adjacent = self.adjacent_points(point)
        return [self.points[adjacent_point] for adjacent_point in adjacent]

    def low_points(self) -> list[int]:
        low_points = []
        for x in range(self.x_limit):
            for y in range(self.y_limit):
                if all(
                        adjacent_depth > self.points[(x, y)]
                        for adjacent_depth
                        in self.adjacent_depths((x, y))
                ):
                    low_points.append((x, y))

        return low_points

    def low_point_depths(self, ):
        return [self.points[point] for point in self.low_points()]

    def basin_sizes(self) -> list[int]:
        sizes = []
        for low_point in self.low_points():
            basin_points = {low_point}
            prev_points = basin_points
            while prev_points:
                print(f"{basin_points=}")
                next_points = set()
                for point in prev_points:
                    next_points = next_points.union(
                        {
                            next_point
                            for next_point in self.adjacent_points(point)
                            if self.points[next_point] < 9
                         }
                    )
                    print(f"{next_points=}")
                next_points = next_points - basin_points
                basin_points = basin_points.union(next_points)
                prev_points = next_points

            sizes.append(len(basin_points))
        return sizes

    def __str__(self):
        output = []
        for y in range(self.y_limit):
            output.append("".join(str(self.points[(x, y)]) for x in range(self.x_limit)))
        return "\n".join(output)


with open("input") as fin:
    lines = [l.strip() for l in fin.readlines()]
    depth_map = DepthMap.from_strings(lines)
    print(depth_map)
    print(depth_map.low_point_depths())
    print(sum(depth + 1 for depth in depth_map.low_point_depths()))

    basin_sizes = sorted(depth_map.basin_sizes(), reverse=True)
    print(basin_sizes[0] * basin_sizes[1] * basin_sizes[2])
