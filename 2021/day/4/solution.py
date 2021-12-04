from typing import Optional


class Board:
    def __init__(self, numbers: list[int], size: int):
        self.numbers = numbers
        self.size = size
        self._marked = [False for number in numbers]

    @classmethod
    def from_lines(cls, lines: list[str]):
        size = len(lines[0].split())
        numbers = [int(num) for line in lines for num in line.split()]
        return cls(numbers, size)

    def mark_number(self, number: int) -> None:
        for pos, board_number in enumerate(self.numbers):
            if board_number == number:
                self._marked[pos] = True

    def is_winner(self) -> bool:
        return any(all(row) for row in self._rows_marked()) \
            or any(all(col) for col in self._cols_marked())

    def calculate_score(self, winning_number: int) -> int:
        return winning_number * sum(
            num for num, marked in zip(self.numbers, self._marked)
            if not marked
        )

    def _rows_marked(self) -> list[list[bool]]:
        return [
            self._marked[i:i+self.size]
            for i in range(0, self.size**2, self.size)
        ]

    def _cols_marked(self) -> list[list[bool]]:
        rows = self._rows_marked()
        return [[row[i] for row in rows] for i in range(self.size)]

    def __str__(self):
        return "\n".join(
            " ".join(
                f"{number:>2}" for number in self.numbers[i:i+self.size]
            )
            for i in range(0, self.size**2, self.size)
        )


def get_winner(boards: list[Board]) -> Optional[Board]:
    for board in boards:
        if board.is_winner():
            return board

    return None


def get_input():
    with open("input") as fin:
        picked_numbers = [int(num) for num in next(fin).split(",")]
        next(fin)

        boards = []
        lines = []
        for line in fin:
            if line == "\n":
                boards.append(Board.from_lines(lines))
                lines = []
                continue

            lines.append(line)

        boards.append(Board.from_lines(lines))
    return picked_numbers, boards


picked_numbers, boards = get_input()
for number in picked_numbers:
    for board in boards:
        board.mark_number(number)

    if winner := get_winner(boards):
        print(winner.calculate_score(number))
        break

picked_numbers, boards = get_input()
last_winners = set()

for number in picked_numbers:
    for board in boards:
        board.mark_number(number)

    current_winners = {board for board in boards if board.is_winner()}
    if len(current_winners) == len(boards):
        last_winner = (current_winners - last_winners).pop()
        print(last_winner.calculate_score(number))
        break
    else:
        last_winners = current_winners
