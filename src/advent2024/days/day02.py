from pathlib import Path


def read_data(data_file: str | Path) -> list[list[int]]:
    with open(data_file, "rt") as infile:
        return [list(map(int, line.strip().split())) for line in infile]


def check_line(line: list[int]) -> bool:
    diffs = [l - r for l, r in zip(line, line[1:])]
    if min(*diffs) >= 1 and max(*diffs) <= 3:
        return True
    elif max(*diffs) <= -1 and min(*diffs) >= -3:
        return True
    else:
        return False


def part1(data_file: str | Path) -> int | str:
    data = read_data(data_file)
    count = 0
    for line in data:
        count += check_line(line)
    return count


def part2(data_file: str | Path) -> int | str:
    data = read_data(data_file)
    count = 0
    for line in data:
        if check_line(line):
            count += 1
            continue

        for i in range(len(line)):
            sline = line[:i] + line[i + 1 :]
            if check_line(sline):
                count += 1
                break

    return count
