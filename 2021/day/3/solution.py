from collections import Counter, defaultdict


def bit_counts(values: list[str]) -> list[Counter]:
    # if values have different lengths, output is undefined
    counts = defaultdict(Counter)

    for value in values:
        for pos, char in enumerate(value):
            counts[pos][char] += 1

    return [counts[k] for k in sorted(counts.keys())]


def gamma_rate(counts: list[Counter]) -> str:
    return "".join(count.most_common(1)[0][0] for count in counts)


def epsilon_rate(counts: list[Counter]) -> str:
    gamma = gamma_rate(counts)
    return "".join("0" if c == "1" else "1" for c in gamma)


def most_common_or_tie(counter: Counter[str], tie_value: str) -> str:
    if counter["0"] > counter["1"]:
        return "0"
    elif counter["1"] > counter["0"]:
        return "1"
    else:
        return tie_value


def least_common_or_tie(counter: Counter[str], tie_value: str) -> str:
    if counter["0"] < counter["1"]:
        return "0"
    elif counter["1"] < counter["0"]:
        return "1"
    else:
        return tie_value


def find_oxygen_rating(values):
    values = list(values)
    for current_position in range(len(values[0])):
        if len(values) == 1:
            break
        counts = Counter(value[current_position] for value in values)
        most_common = most_common_or_tie(counts, "1")
        values = [value for value in values if value[current_position] == most_common]

    return values[0]


def find_scrubber_rating(values):
    values = list(values)
    for current_position in range(len(values[0])):
        if len(values) == 1:
            break
        counts = Counter(value[current_position] for value in values)
        least_common = least_common_or_tie(counts, "0")
        values = [value for value in values if value[current_position] == least_common]

    return values[0]


with open("input") as fin:
    values = [line[:-1] for line in fin]
    counts = bit_counts(values)
    gamma = int(gamma_rate(counts), base=2)
    epsilon = int(epsilon_rate(counts), base=2)
    print(gamma*epsilon)

    oxygen_rating = int(find_oxygen_rating(values), base=2)
    scrubber_rating = int(find_scrubber_rating(values), base=2)
    print(oxygen_rating*scrubber_rating)
