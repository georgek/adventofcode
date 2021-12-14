from collections import Counter


def grow_polymer(template: str, rules: dict[str, str]) -> str:
    pairs = [a+b for a, b in zip(template, template[1:])]
    grown_pairs = [a+rules.get(a+b, "")+b for a, b in pairs]
    return "".join(
        grown_pair[:-1] for grown_pair in grown_pairs
    ) + grown_pairs[-1][-1]


def grow_polymer_fast(pairs: Counter[tuple], rules: dict[str, str]) -> Counter[tuple]:
    new_pairs = Counter()
    for (a, b), count in pairs.items():
        if (a, b) in rules:
            c = rules[(a, b)]
            new_pairs[(a, c)] += pairs[(a, b)]
            new_pairs[(c, b)] += pairs[(a, b)]
        else:
            new_pairs[(a, b)] += pairs[(a, b)]

    return new_pairs


with open("input") as fin:
    template = next(fin).strip()
    next(fin)
    rules = dict(line.strip().split(" -> ") for line in fin)

print(template)
print(rules)

print(f"Template:     {template}")
polymer = template
for step in range(10):
    polymer = grow_polymer(polymer, rules)
    print(f"After step {step+1}: {polymer}")


counter = Counter(polymer)
print(counter.most_common()[0][1] - counter.most_common()[-1][1])

rules = {(ab[0], ab[1]): c for ab, c in rules.items()}

pairs = Counter((a, b) for a, b in zip(template, template[1:]))
for step in range(40):
    pairs = grow_polymer_fast(pairs, rules)

counter = Counter()
for (a, b), count in pairs.items():
    counter[a] += count
counter[template[-1]] += 1
print("After 40 steps:")
print(counter.most_common()[0][1] - counter.most_common()[-1][1])
