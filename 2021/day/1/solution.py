def count_increases(values):
    return sum(b > a for a, b in zip(values, values[1:]))


def windows(values):
    return [a + b + c for a, b, c in zip(values, values[1:], values[2:])]


with open("input") as fin:
    values = [int(line) for line in fin]
    simple_count = count_increases(values)
    print(simple_count)
    window_count = count_increases(windows(values))
    print(window_count)
