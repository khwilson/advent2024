from collections import defaultdict
from pathlib import Path


def read_data(data_file: str | Path) -> list[int]:
    with open(data_file, "rt") as infile:
        return [int(line.strip()) for line in infile]


MOD = (1 << 24) - 1


def step(num: int) -> int:
    num = (num ^ (num << 6)) & MOD
    num = (num ^ (num >> 5)) & MOD
    num = (num ^ (num << 11)) & MOD
    return num


def part1(data_file: str | Path) -> int | str:
    data = read_data(data_file)
    total = 0
    for num in data:
        for _ in range(2000):
            num = step(num)
        total += num
    return total


def part2(data_file: str | Path) -> int | str:
    data = read_data(data_file)
    total = defaultdict(int)
    for num in data:
        prices = [num % 10]
        for _ in range(2000):
            num = step(num)
            prices.append(num % 10)

        diffs = [x - y for x, y in zip(prices[1:], prices)]
        seen: set[tuple[int, int, int, int]] = set()
        for a, b, c, d, p in zip(diffs, diffs[1:], diffs[2:], diffs[3:], prices[4:]):
            if (a, b, c, d) in seen:
                continue
            total[(a, b, c, d)] += p
            seen.add((a, b, c, d))

    return max(total.values())
