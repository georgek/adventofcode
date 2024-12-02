from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class Point:
    x: int
    y: int
    z: int

    @classmethod
    def from_string(cls, string: str) -> Point:
        coords = [int(s) for s in string.split(",")]
        return cls(*coords)

    def rotate(self, multiplier):
        x, y, z = multiplier
        return Point(self.x*x, self.y*y, self.z*z)

    def all_rotations(self) -> list[Point]:
        x_multipliers = [
            (1, 1, 1),
            (1, 1, -1),
            (1, -1, -1),
            (1, -1, 1),
        ]
        y_multipliers = [
            (1, 1, 1),
            (-1, 1, 1),
            (-1, 1, -1),
            (1, 1, -1),
        ]
        z_multipliers = [
            (-1, 1, 1),
            (1, -1, 1),
        ]
        y_rotations = [
            self.rotate(x).rotate(y) for x in x_multipliers for y in y_multipliers
        ]
        z_rotations = [
            self.rotate(x).rotate(z) for x in x_multipliers for z in z_multipliers
        ]
        return y_rotations + z_rotations

    def __add__(self, other) -> Point:
        return Point(self.x+other.x, self.y+other.y, self.z+other.z)

    def __str__(self) -> str:
        return f"{self.x},{self.y},{self.z}"


class BeaconMap:
    def __init__(self, beacons: np.array):
        self.beacons = beacons

    @classmethod
    def from_strings(cls, strings: list[str]) -> BeaconMap:
        beacons = np.array([[int(s) for s in string.split(",")] for string in strings])
        return cls(beacons)

    def all_rotations(self) -> list[BeaconMap]:
        point_rotations = [point.all_rotations() for point in self.beacons]
        return [BeaconMap(beacons) for beacons in zip(*point_rotations)]

    def shift(self, by: Point) -> BeaconMap:
        shifted = [beacon + by for beacon in self.beacons]
        return BeaconMap(shifted)

    def overlaps(self, other: BeaconMap) -> bool:
        for rotation in other.all_rotations():
            for x in range(-500, 501):
                for y in range(-500, 501):
                    for z in range(-500, 501):
                        shifted = rotation.shift(Point(x, y, z))
                        if len(set(self.beacons).intersection(shifted.beacons)) >= 12:
                            return True
        return False

    def __str__(self):
        return "\n".join(str(beacon) for beacon in self.beacons)


beacon_maps = []
with open("test-input") as fin:
    lines = []
    for line in fin:
        if line.startswith("---"):
            continue
        elif line == "\n":
            beacon_maps.append(BeaconMap.from_strings(lines))
            lines = []
        else:
            lines.append(line.strip())
    beacon_maps.append(BeaconMap.from_strings(lines))


for n, beacon_map in enumerate(beacon_maps):
    print(f"--- scanner {n} ---")
    print(beacon_map)
    print()
