#!/usr/bin/env python


def n_safe(lines: list[str], tolerant: bool = False) -> int:
    return sum(is_safe(line, tolerant=tolerant) for line in lines)


def is_safe(line: str, tolerant: bool = False) -> bool:
    report = [int(i) for i in line.split()]

    safe = is_consistent(report) and is_steady(report)

    if safe:
        return True

    if tolerant:
        for i in range(len(report)):
            r = list(report)
            del r[i]
            safe = is_consistent(r) and is_steady(r)
            if safe:
                return True

    return False


def is_consistent(report: list[int]) -> bool:
    return all(n > 0 for n in diffs(report)) or all(n < 0 for n in diffs(report))


def is_steady(report: list[int]) -> bool:
    return all(abs(n) >= 1 and abs(n) <= 3 for n in diffs(report))


def diffs(report: list[int]) -> list[int]:
    return [i-j for i, j in zip(report[1:], report[:-1])]



def main():
    with open("input") as fin:
        lines = fin.readlines()

    print("Safe reports:", n_safe(lines))
    print("Safe reports (tolerant):", n_safe(lines, tolerant=True))


if __name__ == '__main__':
    main()
