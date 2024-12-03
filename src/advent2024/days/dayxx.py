from pathlib import Path


def read_data(data_file: str | Path) -> None:
    with open(data_file, "rt") as infile:
        pass


def part1(data_file: str | Path) -> int | str:
    data = read_data(data_file)
    return 10


def part2(data_file: str | Path) -> int | str:
    data = read_data(data_file)
    return 10
