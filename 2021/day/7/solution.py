def fuel_needed(positions: list[int], target: int) -> int:
    return sum(abs(position-target) for position in positions)


def fuel_needed_new(positions: list[int], target: int) -> int:
    def trig(n):
        return (n*(n+1))//2

    return sum(trig(abs(position-target)) for position in positions)


with open("test-input") as fin:
    positions = [int(pos) for pos in next(fin).strip().split(",")]

print(positions)
print(min(fuel_needed(positions, target) for target in range(max(positions))))
print(min(fuel_needed_new(positions, target) for target in range(max(positions))))
