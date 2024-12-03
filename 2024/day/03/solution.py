#!/usr/bin/env python

import re


def main():
    with open("input") as fin:
        input = fin.read()

    print(calc(input))
    print(calc_conditional(input))


def calc(input: str) -> int:
    sum = 0
    while input:
        if match := re.match(r"^mul\(([0-9]{1,3}),([0-9]{1,3})\)", input):
            input = input[len(match[0])-1:]
            sum += int(match[1]) * int(match[2])
        input = input[1:]

    return sum


def calc_conditional(input: str) -> int:
    sum = 0
    doing = True
    while input:
        if match := re.match(
                r"^(?P<op>mul|do|don't)\(((?P<x>[0-9]{1,3}),(?P<y>[0-9]{1,3}))?\)",
                input,
        ):
            match match.groupdict():
                case {"op": "mul", "x": x, "y": y}:
                    if doing:
                        sum += int(x) * int(y)
                case {"op": "do"}:
                    doing = True
                case {"op": "don't"}:
                    doing = False
            input = input[len(match[0])-1:]
        input = input[1:]

    return sum


if __name__ == '__main__':
    main()
