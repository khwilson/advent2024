from pathlib import Path

from tqdm.auto import tqdm

DIRS = {
    ">": (0, 1),
    "<": (0, -1),
    "^": (-1, 0),
    "v": (1, 0),
}

TURN = {
    ">": "v",
    "v": "<",
    "<": "^",
    "^": ">",
}


def read_data(data_file: str | Path) -> list[list[str]]:
    with open(data_file, "rt") as infile:
        return [[x for x in line.strip()] for line in infile]


def step(
    data: list[list[str | set[str]]], pos: tuple[int, int], cur_dir: str
) -> tuple[int, int, str] | None:
    drow, dcol = DIRS[cur_dir]
    row, col = pos
    next_row, next_col = row + drow, col + dcol

    # Check if out of bounds
    if not ((0 <= next_row < len(data)) and (0 <= next_col < len(data[0]))):
        return None

    if data[next_row][next_col] == "#":
        return step(data, pos, TURN[cur_dir])

    return next_row, next_col, cur_dir


def part1(data_file: str | Path) -> int | str:
    data = read_data(data_file)
    start_pos = (-1, -1)
    for i, line in enumerate(data):
        for j, val in enumerate(line):
            if val in DIRS:
                cur_dir = val
                start_pos = (i, j)
                break
        if start_pos != (-1, -1):
            break

    count = 1
    pos = start_pos
    data[start_pos[0]][start_pos[1]] = "X"

    while True:
        next = step(data, pos, cur_dir)
        if not next:
            break

        row, col, cur_dir = next
        pos = (row, col)
        if data[row][col] == ".":
            count += 1
            data[row][col] = "X"

    return count


def part2(data_file: str | Path) -> int | str:
    data = read_data(data_file)
    start_pos = (-1, -1)
    for i, line in enumerate(data):
        for j, val in enumerate(line):
            if val in DIRS:
                start_dir = val
                start_pos = (i, j)
                break
        if start_pos != (-1, -1):
            break

    data: list[list[str | set[str]]] = [
        [set() if val != "#" else "#" for val in line] for line in data
    ]

    # Brute force! There's probably some nicer ways to do this, e.g.,
    # by making the adjacency graph of obstructions and trying to
    # detect cycles (which would run in time O(# obstructions) per cycle
    # Given there are ≈800 obstructions in the data of a 16k grid,
    # that would likely speed this up considerably! But calculating
    # the adjacency matrix requires more thought :-)
    count = 0
    raw_data = data
    for new_row in tqdm(range(len(data))):
        for new_col in range(len(data[0])):
            data = [
                [val if isinstance(val, str) else set() for val in line]
                for line in raw_data
            ]
            data[new_row][new_col] = "#"
            pos = start_pos
            cur_dir = start_dir

            while True:
                next = step(data, pos, cur_dir)
                if not next:
                    break

                row, col, cur_dir = next
                pos = (row, col)
                if data[row][col] != "#":
                    if cur_dir in data[row][col]:
                        count += 1
                        break

                    data[row][col].add(cur_dir)

    return count
