from itertools import chain, groupby
from functools import reduce


SEGMENT_TO_DECIMAL = {
    "abcefg": "0",
    "cf": "1",
    "acdeg": "2",
    "acdfg": "3",
    "bcdf": "4",
    "abdfg": "5",
    "abdefg": "6",
    "acf": "7",
    "abcdefg": "8",
    "abcdfg": "9",
}


def decode_input_line(line: str):
    segments, values = line.strip().split(" | ")
    return segments.split(), values.split()


def common_element(strings, exclude: set = None):
    if exclude is None:
        exclude = set()
    common = set.intersection(*[set(s) - exclude for s in strings])
    if len(common) > 1:
        raise Exception("Too many elements in common", common)
    return common.pop()


def figure_out_segments(segments: list[str]):
    sorted_segments = sorted(segments, key=lambda seg: len(seg))
    grouper = groupby(sorted_segments, lambda seg: len(seg))
    groups = {key: list(vals) for key, vals in grouper}

    one = groups[2][0]
    four = groups[4][0]
    seven = groups[3][0]
    eight = groups[7][0]

    a = common_element(chain.from_iterable(groups[k] for k in [6, 5, 3, 7]))
    d = common_element(chain.from_iterable(groups[k] for k in [5, 4]))
    g = common_element(chain.from_iterable(groups[k] for k in [6, 5, 7]), exclude={a})

    b = set(four) - set(one) - set(d)
    assert len(b) == 1
    b = b.pop()

    f = common_element(chain(groups[6], [one]))

    c = set(one) - {f}
    assert len(c) == 1
    c = c.pop()

    e = set(eight) - {a, b, c, d, f, g}
    assert len(e) == 1
    e = e.pop()

    return {
        a: "a",
        b: "b",
        c: "c",
        d: "d",
        e: "e",
        f: "f",
        g: "g",
    }


def decode_value(decoder: dict[str, str], value: list[str]) -> int:
    return int("".join(decode_digit(decoder, digit) for digit in value))


def decode_digit(decoder: dict[str, str], digit: str) -> str:
    decoded_segments = "".join(sorted(decoder[seg] for seg in digit))
    return SEGMENT_TO_DECIMAL[decoded_segments]


with open("input") as fin:
    input_values = [decode_input_line(line) for line in fin]
    segment_lists, value_lists = zip(*input_values)

    all_values = reduce(lambda x, y: x+y, value_lists, [])

decimal_values = []
for segments, values in zip(segment_lists, value_lists):
    decoder = figure_out_segments(segments)
    decoded_value = decode_value(decoder, values)
    decimal_values.append(decoded_value)

print(sum(decimal_values))
