def calculate_position(instructions: list[str]) -> tuple[int, int]:
    horizontal = 0
    depth = 0
    for instruction in instructions:
        match instruction.split():
            case ["forward", amount]:
                horizontal += int(amount)
            case ["down", amount]:
                depth += int(amount)
            case ["up", amount]:
                depth -= int(amount)

    return horizontal, depth


def calculate_position_new(instructions: list[str]) -> tuple[int, int]:
    horizontal = 0
    depth = 0
    aim = 0
    for instruction in instructions:
        match instruction.split():
            case ["forward", amount]:
                horizontal += int(amount)
                depth += aim*int(amount)
            case ["down", amount]:
                aim += int(amount)
            case ["up", amount]:
                aim -= int(amount)

    return horizontal, depth


with open("input") as fin:
    horizontal, depth = calculate_position(fin)
    print(horizontal * depth)

with open("input") as fin:
    horizontal, depth = calculate_position_new(fin)
    print(horizontal * depth)
