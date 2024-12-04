from pathlib import Path


def go_in_dir(
    x: int, y: int, dx: int, dy: int, max_x: int, max_y: int
) -> tuple[int, int] | None:
    xx = x + dx
    yy = y + dy
    if xx >= 0 and xx < max_x and yy >= 0 and yy < max_y:
        return xx, yy
    return None


def eight_ways() -> list[tuple[int, int]]:
    out: list[tuple[int, int]] = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == j == 0:
                continue
            out.append((i, j))
    return out


def eight_ways_(x: int, y: int, max_x: int, max_y: int) -> list[tuple[int]]:
    out = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == j == 0:
                continue
            out.append((x + i), (y + j))
    out = [
        (xx, yy) for xx, yy in out if xx >= 0 and xx < max_x and yy >= 0 and yy < max_y
    ]
    return out


def read_data(data_file: str | Path) -> list[list[str]]:
    with open(data_file, "rt") as infile:
        return [line.strip() for line in infile]


def part1(data_file: str | Path) -> int | str:
    data = read_data(data_file)
    max_x = len(data)
    max_y = len(data[0])
    starts: list[tuple[int, int, int, int]] = []
    counter = 0
    for i, row in enumerate(data):
        for j, val in enumerate(row):
            if val != "X":
                continue
            for next_i, next_j in eight_ways():
                starts.append((i, j, next_i, next_j))

    for i, j, di, dj in starts:
        for letter in "XMAS":
            if data[i][j] != letter:
                break
            step = go_in_dir(i, j, di, dj, max_x, max_y)
            if step:
                i, j = step

        else:
            counter += 1

    return counter


def part2(data_file: str | Path) -> int | str:
    data = read_data(data_file)
    max_x = len(data)
    max_y = len(data[0])
    starts: list[tuple[int, int]] = []
    counter = 0
    for i, row in enumerate(data):
        for j, val in enumerate(row):
            if val != "A":
                continue
            starts.append((i, j))

    for i, j in starts:
        ul = go_in_dir(i, j, -1, -1, max_x, max_y)
        ur = go_in_dir(i, j, -1, 1, max_x, max_y)
        dl = go_in_dir(i, j, 1, -1, max_x, max_y)
        dr = go_in_dir(i, j, 1, 1, max_x, max_y)

        # X has to be possible
        if not (ul and ur and dl and dr):
            continue

        one = {data[ul[0]][ul[1]], data[dr[0]][dr[1]]}
        two = {data[ur[0]][ur[1]], data[dl[0]][dl[1]]}
        if one == {"M", "S"} and two == {"M", "S"}:
            counter += 1

    return counter
