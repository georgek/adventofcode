import re


def highest_point(x_vel, y_vel, x_min, x_max, y_min, y_max):
    probe_x, probe_y = 0, 0
    highest_point = 0
    while probe_x < x_max and probe_y > y_min:
        probe_x += x_vel
        probe_y += y_vel
        x_vel = max(0, x_vel-1)
        y_vel -= 1
        highest_point = max(highest_point, probe_y)

        if x_min <= probe_x <= x_max and y_min <= probe_y <= y_max:
            return highest_point

    return None


with open("input") as fin:
    line = next(fin).strip()
    match = re.match(r"target area: x=(-?\d+)..(-?\d+), y=(-?\d+)..(-?\d+)", line)
    x_min, x_max, y_min, y_max = [int(s) for s in match.groups()]
    print(x_min, x_max, y_min, y_max)

highest = 0
on_target = []
for x in range(1, x_max+1):     # because any higher x would overshoot immediately
    for y in range(y_min, 1000):  # meh... can't prove this is the right number to go to
        current_highest = highest_point(x, y, x_min, x_max, y_min, y_max)
        if current_highest is not None:
            highest = max(highest, current_highest)
            on_target.append((x, y))

print(highest)
print(len(on_target))
