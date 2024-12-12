from functools import lru_cache
from pathlib import Path


@lru_cache(maxsize=None)
def recurse(val: str, depth: int) -> int:
    if depth == 0:
        return 1

    if val == "0":
        return recurse("1", depth - 1)

    if len(val) % 2 == 0:
        return recurse(str(int(val[: len(val) // 2])), depth - 1) + recurse(
            str(int(val[len(val) // 2 :])), depth - 1
        )

    return recurse(str(int(val) * 2024), depth - 1)


def read_data(data_file: str | Path) -> list[str]:
    with open(data_file, "rt") as infile:
        return infile.read().strip().split()


def part1(data_file: str | Path) -> int | str:
    data = read_data(data_file)
    return sum(recurse(val, depth=25) for val in data)


def part2(data_file: str | Path) -> int | str:
    data = read_data(data_file)
    return sum(recurse(val, depth=75) for val in data)
