from functools import cache
from pathlib import Path


def read_data(data_file: str | Path) -> tuple[list[str], list[str]]:
    with open(data_file, "rt") as infile:
        patterns = next(infile).strip().split(", ")
        next(infile)
        desired = [line.strip() for line in infile]

    return patterns, desired


@cache
def rec(desired: str, patterns: frozenset[str]) -> bool:
    if not desired:
        return True

    for p in patterns:
        if desired.startswith(p):
            if rec(desired[len(p) :], patterns):
                return True

    return False


def part1(data_file: str | Path) -> int | str:
    patterns, desired = read_data(data_file)
    patterns = frozenset(patterns)
    return sum(rec(d, patterns) for d in desired)


@cache
def rec2(desired: str, patterns: frozenset[str]) -> int:
    if not desired:
        return 1

    total = 0
    for p in patterns:
        if desired.startswith(p):
            val = rec2(desired[len(p) :], patterns)
            if val:
                total += val

    return total


def part2(data_file: str | Path) -> int | str:
    patterns, desired = read_data(data_file)
    patterns = frozenset(patterns)
    return sum(rec2(d, patterns) for d in desired)
