import re
from pathlib import Path


def read_data(data_file: str | Path) -> list[str]:
    with open(data_file, "rt") as infile:
        return [line.strip() for line in infile]


def part1(data_file: str | Path) -> int | str:
    data = read_data(data_file)
    total = 0
    for line in data:
        for mul_val in re.findall(r"mul\(\d{1,3},\d{1,3}\)", line):
            left, right = map(int, mul_val[4:-1].split(","))
            total += left * right
    return total


def part2(data_file: str | Path) -> int | str:
    data = read_data(data_file)
    total = 0
    enabled = True
    for line in data:
        for mul_or_do_val in re.findall(r"(mul\(\d{1,3},\d{1,3}\)|do(n't)?\(\))", line):
            mul_or_do_val = mul_or_do_val[0]
            if mul_or_do_val == "don't()":
                enabled = False
            elif mul_or_do_val == "do()":
                enabled = True
            elif enabled:
                left, right = map(int, mul_or_do_val[4:-1].split(","))
                total += left * right

    return total
