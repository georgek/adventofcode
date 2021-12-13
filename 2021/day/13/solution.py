from dataclasses import dataclass


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    @classmethod
    def fromstring(cls, string: str):
        x, y = string.split(",")
        return cls(int(x), int(y))


class Paper:
    def __init__(self, dots: list[Point], right: int, bottom: int):
        self.dots = set(dots)
        self.left = 0
        self.right = right
        self.top = 0
        self.bottom = bottom

    @classmethod
    def fromstrings(cls, strings: list[str]):
        dots = [Point.fromstring(string) for string in strings]
        left = max(dot.x for dot in dots)
        bottom = max(dot.y for dot in dots)
        return cls(dots, left, bottom)

    def fold_up(self, y: int) -> None:
        abs_y = self.top + y
        for dot in list(self.dots):
            if dot.y > abs_y:
                self.dots.remove(dot)
                self.dots.add(Point(dot.x, abs_y-(dot.y-abs_y)))

        self.bottom = abs_y - 1
        print(self.top)
        self.top = min(self.bottom-y+1, self.top)
        print(self.top)

    def fold_across(self, x: int) -> None:
        abs_x = self.left + x
        for dot in list(self.dots):
            if dot.x < abs_x:
                self.dots.remove(dot)
                self.dots.add(Point(abs_x+(abs_x-dot.x), dot.y))

        self.left = abs_x + 1
        print(self.right)
        self.right = max(self.left+x-1, self.right)
        print(self.right)

    def __str__(self) -> str:
        return "\n".join(
            "".join(
                "#" if Point(x, y) in self.dots else " "
                for x in range(self.left, self.right+1)
            )
            for y in range(self.top, self.bottom+1)
        )


with open("input") as fin:
    lines = [line.strip() for line in fin]
    sep = lines.index("")
    dots = lines[:sep]
    folds = lines[sep+1:]

print(dots)
print(folds)
paper = Paper.fromstrings(dots)
print(paper)

for fold in folds[:1]:
    print(fold)
    direction, position = fold.split()[-1].split("=")
    if direction == "x":
        paper.fold_across(int(position))
    else:
        paper.fold_up(int(position))
    print(len(paper.dots))

paper = Paper.fromstrings(dots)

for fold in folds:
    print(fold)
    direction, position = fold.split()[-1].split("=")
    if direction == "x":
        paper.fold_across(int(position))
    else:
        paper.fold_up(int(position))

print(paper)
