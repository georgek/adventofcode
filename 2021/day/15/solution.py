from __future__ import annotations

import heapq
import math
from dataclasses import dataclass


@dataclass(frozen=True, order=True)
class Point:
    x: int
    y: int


class Map:
    def __init__(self, points: dict[Point, int], dimensions: tuple[int, int]):
        self.points = points
        self.x_limit, self.y_limit = dimensions

    @classmethod
    def from_strings(cls, strings: list[str]) -> Map:
        y_limit = len(strings)
        points = {}
        for y, string in enumerate(strings):
            x_limit = len(string)
            for x, char in enumerate(string):
                points[Point(x, y)] = int(char)

        return cls(points, (x_limit, y_limit))

    def supermap(self) -> Map:
        points = {}
        for i in range(5):
            for j in range(5):
                for point, value in self.points.items():
                    points[
                        Point(point.x + i * self.x_limit, point.y + j * self.y_limit)
                    ] = (self.points[point] + i + j - 1) % 9 + 1

        return Map(points, (self.x_limit * 5, self.y_limit * 5))

    def adjacent_points(self, point: tuple[int, int]) -> set[tuple]:
        adjacent = set()
        if point.x > 0:
            adjacent.add(Point(point.x - 1, point.y))
        if point.x < self.x_limit - 1:
            adjacent.add(Point(point.x + 1, point.y))
        if point.y > 0:
            adjacent.add(Point(point.x, point.y - 1))
        if point.y < self.y_limit - 1:
            adjacent.add(Point(point.x, point.y + 1))

        return adjacent

    def heuristic(self, point: Point) -> int:
        """Euclidean distance to bottom-right"""
        return math.sqrt(
            (self.x_limit - point.x - 1) ** 2 + (self.y_limit - point.y - 1) ** 2
        )

    def shortest_path(self, point_from: Point, point_to: Point) -> int:
        """A* algorithm"""
        unvisited = set(self.points.keys())
        g_distances = {point: math.inf for point in self.points}
        g_distances[point_from] = 0
        h_distances = {point: math.inf for point in self.points}
        h_distances[point_from] = self.heuristic(point_from)
        h_distances = [(val, key) for key, val in h_distances.items()]
        heapq.heapify(h_distances)

        while point_to in unvisited:
            while smallest := heapq.heappop(h_distances):
                _, current_point = smallest
                if current_point in unvisited:
                    break
            for adjacent in self.adjacent_points(current_point).intersection(unvisited):
                dist_through_current = (
                    g_distances[current_point] + self.points[adjacent]
                )
                if dist_through_current < g_distances[adjacent]:
                    g_distances[adjacent] = dist_through_current
                    h_distance = dist_through_current + self.heuristic(adjacent)
                    heapq.heappush(h_distances, (h_distance, adjacent))

            unvisited.remove(current_point)

        return g_distances[point_to]

    def get_point_string(self, point: Point) -> str:
        max_len = max(len(str(val)) for val in self.points.values() if val < math.inf)
        if self.points[point] < math.inf:
            string = str(self.points[point])
        else:
            string = "."

        return f"{string:>{max_len+1}}"

    def __str__(self):
        output = []
        for y in range(self.y_limit):
            output.append(
                "".join(
                    str(self.get_point_string(Point(x, y))) for x in range(self.x_limit)
                )
            )
        return "\n".join(output)


with open("input") as fin:
    lines = fin.read().split()

risk_map = Map.from_strings(lines)

shortest_path = risk_map.shortest_path(
    Point(0, 0),
    Point(risk_map.x_limit - 1, risk_map.y_limit - 1),
)
print(shortest_path)

supermap = risk_map.supermap()

shortest_path = supermap.shortest_path(
    Point(0, 0),
    Point(supermap.x_limit - 1, supermap.y_limit - 1),
)
print(shortest_path)
