import itertools as its
from pathlib import Path


def read_data(data_file: str | Path) -> tuple[list[list[str]], list[list[str]]]:
    keys: list[list[str]] = []
    locks: list[list[str]] = []
    with open(data_file, "rt") as infile:
        current = []
        for line in infile:
            line = line.strip()
            if not line:
                if current[0][0] == ".":
                    keys.append(current)
                elif current[0][0] == "#":
                    locks.append(current)
                else:
                    raise ValueError
                current = []
            else:
                current.append(line)
    if current:
        if current[0][0] == ".":
            keys.append(current)
        elif current[0][0] == "#":
            locks.append(current)
        else:
            raise ValueError
    return locks, keys


def part1(data_file: str | Path) -> int | str:
    locks, keys = read_data(data_file)
    lock_heights = []
    key_heights = []
    for lock in locks:
        out = [-1] * len(lock[0])
        for row in lock:
            for i, val in enumerate(row):
                out[i] += val == "#"
        lock_heights.append(out)

    for key in keys:
        out = [-1] * len(key[0])
        for row in key:
            for i, val in enumerate(row):
                out[i] += val == "#"
        key_heights.append(out)

    count = 0
    for lock, key in its.product(lock_heights, key_heights):
        if all(l + k <= 5 for l, k in zip(lock, key)):
            count += 1

    return count


def part2(data_file: str | Path) -> int | str:
    return "DONE!"
