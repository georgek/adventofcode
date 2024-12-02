from __future__ import annotations

import time
import math
from typing import TypeVar
from itertools import permutations

T = TypeVar("T")


def left(t: list[T]) -> T:
    return t[0]


def right(t: list[T]) -> T:
    return t[1]


class SnailNumber:
    def __init__(self, numbers: list[int], depths: list[int]):
        self.numbers = numbers
        self.depths = depths
        self._reduce()

    @classmethod
    def from_string(cls, string: str) -> SnailNumber:
        current_depth = 0
        numbers = []
        depths = []
        for char in string:
            if char == "[":
                current_depth += 1
            elif char == "]":
                current_depth -= 1
            elif char != ",":
                number = int(char)
                numbers.append(number)
                depths.append(current_depth)

        return cls(numbers, depths)

    def magnitude(self) -> int:
        numdepths = list(zip(self.numbers, self.depths))
        while len(numdepths) > 1:
            print(numdepths)
            skip = False
            new_numdepths = []
            for (num1, dep1), (num2, dep2) in zip(numdepths, numdepths[1:]):
                if skip:
                    skip = False
                    continue
                if dep1 == dep2:
                    skip = True
                    new_numdepths.append((3*num1+2*num2, dep1-1))
                else:
                    new_numdepths.append((num1, dep1))
            if not skip:
                new_numdepths.append((num2, dep2))
            numdepths = new_numdepths

        return numdepths[0][0]

    def __add__(self, other: SnailNumber) -> SnailNumber:
        new_numbers = self.numbers + other.numbers
        new_depths = [depth+1 for depth in self.depths+other.depths]
        return SnailNumber(new_numbers, new_depths)

    def _reduce(self):
        work = True
        while work:
            print(self.numbers)
            print(self.depths)
            work = self._explode1() or self._split1()

    def _explode1(self):
        for n, (dep1, dep2) in enumerate(zip(self.depths, self.depths[1:])):
            if dep1 == dep2 and dep1 > 4:
                break
        else:
            return False
        print("explode")
        new_numbers = self.numbers[:n] + [0] + self.numbers[n+2:]
        new_depths = self.depths[:n] + [self.depths[n]-1] + self.depths[n+2:]
        if n > 0:
            new_numbers[n-1] = new_numbers[n-1] + self.numbers[n]
        if n < len(self.numbers)-2:
            new_numbers[n+1] = new_numbers[n+1] + self.numbers[n+1]
        self.numbers = new_numbers
        self.depths = new_depths
        assert len(self.numbers) == len(self.depths)
        return True

    def _split1(self):
        for n, num in enumerate(self.numbers):
            if num >= 10:
                break
        else:
            return False
        print("split")
        new_numbers = (
            self.numbers[:n]
            + [math.floor(self.numbers[n]/2), math.ceil(self.numbers[n]/2)]
            + self.numbers[n+1:]
        )
        new_depths = (
            self.depths[:n]
            + [self.depths[n]+1, self.depths[n]+1]
            + self.depths[n+1:]
        )
        self.numbers = new_numbers
        self.depths = new_depths
        assert len(self.numbers) == len(self.depths)
        return True

    def __str__(self):
        # meant to be reverse of from_string, but doesn't work properly (maybe not
        # possible)
        return ",".join(str(n) for n in self.numbers)
        # chars = []
        # current_depth = 0
        # for number, depth in zip(self.numbers, self.depths):
        #     while depth < current_depth:
        #         chars.append("]")
        #         current_depth -= 1
        #     while depth > current_depth:
        #         chars.append("[")
        #         current_depth += 1
        #     chars.append(str(number))
        #     chars.append(",")
        # while current_depth > 0:
        #     chars.pop()
        #     chars.append("]")
        #     current_depth -= 1
        # return "".join(chars)


with open("test-input") as fin:
    lines = [line.strip() for line in fin]

numbers = [SnailNumber.from_string(line) for line in lines]
# sum = numbers[0]
# for number in numbers[1:]:
#     sum = sum + number

# print(sum.magnitude())

n = SnailNumber.from_string("[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]") + SnailNumber.from_string("[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]")

# n = SnailNumber.from_string("[[[[0,7],[8,8],[0,6]],[9,6],[[6,6],[7,0],[8,9]]]]")
# n.magnitude()

# max_sum = 0
# for num1, num2 in permutations(numbers, 2):
#     print(num1, num2)
#     sum = num1+num2
#     max_sum = max(max_sum, sum.magnitude())

# print(max_sum)
