#!/usr/bin/env python


def main():
    with open("input") as fin:
        lines = fin.readlines()

    print(num_words(lines, "XMAS"))


def num_words(lines: list[str], word: str) -> int:
    num = 0

    num += sum(num_words_line(line, word) for line in lines)
    num += sum(num_words_line(line[::-1], word) for line in lines)
    num += sum(num_words_line(line, word) for line in transpose(lines))
    num += sum(num_words_line(line[::-1], word) for line in transpose(lines))
    num += sum(num_words_line(line, word) for line in skew_up(lines))
    num += sum(num_words_line(line[::-1], word) for line in skew_up(lines))
    num += sum(num_words_line(line, word) for line in skew_down(lines))
    num += sum(num_words_line(line[::-1], word) for line in skew_down(lines))

    return num


def num_words_line(line: str, word: str) -> int:
    return sum(line[n:n+len(word)] == word for n in range(len(line)-len(word)))


def transpose(lines: list[str]) -> list[str]:
    return ["".join(line[i] for line in lines) for i in range(len(lines[0]))]


def skew_up(lines: list[str]) -> list[str]:
    l = len(lines[0])
    padded_lines = [" "*(l-i-1)+line+" "*(i) for i, line in enumerate(lines)]
    return transpose(padded_lines)


def skew_down(lines: list[str]) -> list[str]:
    l = len(lines[0])
    padded_lines = [" "*(i)+line+" "*(l-i-1) for i, line in enumerate(lines)]
    return transpose(padded_lines)


if __name__ == '__main__':
    main()
