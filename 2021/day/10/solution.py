PAIRS = {
    "(": ")",
    "[": "]",
    "{": "}",
    "<": ">",
}

ERROR_POINTS = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137,
}

COMPLETION_POINTS = {
    ")": 1,
    "]": 2,
    "}": 3,
    ">": 4,
}


class DecodeError(Exception):
    def __init__(self, illegal_char: str):
        super().__init__()
        self.illegal_char = illegal_char


def decode_chunks(string: str) -> list[str]:
    openings = []
    for char in string:
        if char in PAIRS:
            openings.append(char)
        elif PAIRS[openings[-1]] == char:
            openings.pop()
        else:
            raise DecodeError(char)

    return "".join(PAIRS[char] for char in reversed(openings))


def completion_score(string: str) -> int:
    score = 0
    for char in string:
        score *= 5
        score += COMPLETION_POINTS[char]

    return score


with open("input") as fin:
    lines = [line.strip() for line in fin.readlines()]

illegal_chars = []
completion_scores = []
for line in lines:
    try:
        completion = decode_chunks(line)
        completion_scores.append(completion_score(completion))
    except DecodeError as exc:
        illegal_chars.append(exc.illegal_char)


print(sum(ERROR_POINTS[char] for char in illegal_chars))
completion_scores.sort()
print(completion_scores[len(completion_scores)//2])
