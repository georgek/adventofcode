#!/usr/bin/env python

from collections import Counter


def int_lists(lines: str) -> tuple[list[int], list[int]]:
    left, right = zip(*(line.split() for line in lines))

    return sorted_int_list(left), sorted_int_list(right)


def sorted_int_list(list: list[str]) -> list[int]:
    return sorted([int(i) for i in list])


def distance(left: list[int], right: list[int]) -> int:
    return sum(abs(int(l) - int(r)) for l, r in zip(left, right))


def similarity(left: list[int], right: list[int]) -> int:
    counts = Counter(right)

    return sum(n*counts[n] for n in left)



def main():
    with open("input") as fin:
        lines = fin.readlines()

    left, right = int_lists(lines)

    print("Distance:", distance(left, right))
    print("Similarity:", similarity(left, right))


if __name__ == '__main__':
    main()
