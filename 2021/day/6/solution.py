from collections import Counter, defaultdict


def next_fish(fish: int) -> int:
    return (fish-1) % 7 if fish < 7 else fish-1


def next_day(fishes: list[int]) -> list[int]:
    next_fishes = [next_fish(fish) for fish in fishes]
    new_fishes = [8 for fish in fishes if fish == 0]

    return next_fishes + new_fishes


def next_day_fast(fishes: dict[int, int]) -> dict[int, int]:
    next_fishes = defaultdict(int)
    for fish, count in fishes.items():
        next_fishes[next_fish(fish)] += count
    next_fishes[8] = fishes.get(0, 0)
    return next_fishes


with open("test-input") as fin:
    fishes = [int(string) for string in next(fin).split(",")]

print("Initial state:", ",".join(str(fish) for fish in fishes))
for day in range(1, 18+1):
    fishes = next_day(fishes)
    print(f"After {day:>2} days:", ",".join(str(fish) for fish in fishes))

with open("input") as fin:
    fishes = [int(string) for string in next(fin).split(",")]
    fishes = Counter(fishes)

for day in range(256):
    fishes = next_day_fast(fishes)

print(sum(count for count in fishes.values()))
