import itertools as its
from collections import defaultdict, deque
from pathlib import Path

from tqdm.auto import tqdm


def read_data(data_file: str | Path) -> list[list[str]]:
    maze: list[list[str]] = []
    with open(data_file, "rt") as infile:
        for line in infile:
            maze.append([val for val in line.strip()])
    return maze


def four_ways(x: int, y: int, max_x: int, max_y: int) -> list[tuple[int, int]]:
    out = []
    for i, j in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        out.append(((x + i), (y + j)))
    out = [
        (xx, yy) for xx, yy in out if xx >= 0 and xx < max_x and yy >= 0 and yy < max_y
    ]
    return out


def twenty_ways(x: int, y: int, max_x: int, max_y: int) -> list[tuple[int, int]]:
    out: list[tuple[int, int]] = []
    for i in range(-20, 21):
        max_j = 20 - abs(i)
        for j in range(-max_j, max_j + 1):
            xx = x + i
            yy = y + j
            if 0 <= xx < max_x and 0 <= yy < max_y:
                out.append((xx, yy))
    return out


def part1(data_file: str | Path, is_part_two: bool = False) -> int | str:
    maze = read_data(data_file)
    height = len(maze)
    width = len(maze[0])

    start: tuple[int, int] | None = None
    end: tuple[int, int] | None = None
    for i in range(1, height - 1):
        for j in range(1, width - 1):
            if maze[i][j] == "S":
                start = (i, j)
            elif maze[i][j] == "E":
                end = (i, j)
        if start and end:
            break

    # Find all distances from `end` to every other point
    dist_to_end: dict[tuple[int, int], int] = {end: 0}

    # (point, distance from end)
    queue = deque([(end, 0)])
    while queue:
        (row, col), length = queue.popleft()

        for i, j in four_ways(row, col, height, width):
            if maze[i][j] in [".", "S"] and (i, j) not in dist_to_end:
                dist_to_end[(i, j)] = length + 1
                queue.append(((i, j), length + 1))


    # Compute all distances from `start` to every other point`
    dist_from_start: dict[tuple[int, int], int] = {start: 0}
    queue = deque([(start, 0)])
    while queue:
        (row, col), length = queue.popleft()

        for i, j in four_ways(row, col, height, width):
            if maze[i][j] in [".", "E"] and (i, j) not in dist_from_start:
                dist_from_start[(i, j)] = length + 1
                queue.append(((i, j), length + 1))

    the_dist = dist_from_start[end]

    savings: dict[tuple[int, int], int] = defaultdict(int)
    for row in tqdm(range(1, height - 1)):
        for col in range(1, width - 1):
            if maze[i][j] != "#":
                continue

            xx = four_ways(row, col, height, width)
            for (lx, ly), (rx, ry) in its.combinations(xx, 2):
                if maze[lx][ly] != "#" and maze[rx][ry] != "#":
                    # import ipdb; ipdb.set_trace()
                    savings[(row, col)] = max(savings[(row, col)], the_dist - (dist_from_start[(lx, ly)] + dist_to_end[(rx, ry)] + 1))
                    savings[(row, col)] = max(savings[(row, col)], the_dist - (dist_to_end[(lx, ly)] + dist_from_start[(rx, ry)] + 1))

    return sum(1 for val in savings.values() if val >= 100)


def part2(data_file: str | Path) -> int | str:
    maze = read_data(data_file)
    height = len(maze)
    width = len(maze[0])

    start: tuple[int, int] | None = None
    end: tuple[int, int] | None = None
    for i in range(1, height - 1):
        for j in range(1, width - 1):
            if maze[i][j] == "S":
                start = (i, j)
            elif maze[i][j] == "E":
                end = (i, j)
        if start and end:
            break

    # Find all distances from `end` to every other point
    dist_to_end: dict[tuple[int, int], int] = {end: 0}

    # (point, distance from end)
    queue = deque([(end, 0)])
    while queue:
        (row, col), length = queue.popleft()

        for i, j in four_ways(row, col, height, width):
            if maze[i][j] in [".", "S"] and (i, j) not in dist_to_end:
                dist_to_end[(i, j)] = length + 1
                queue.append(((i, j), length + 1))


    # Compute all distances from `start` to every other point`
    dist_from_start: dict[tuple[int, int], int] = {start: 0}
    queue = deque([(start, 0)])
    while queue:
        (row, col), length = queue.popleft()

        for i, j in four_ways(row, col, height, width):
            if maze[i][j] in [".", "E"] and (i, j) not in dist_from_start:
                dist_from_start[(i, j)] = length + 1
                queue.append(((i, j), length + 1))

    the_dist = dist_from_start[end]

    savings: dict[tuple[int, int], int] = defaultdict(int)
    for row in tqdm(range(1, height - 1)):
        for col in range(1, width - 1):
            if maze[i][j] != "#":
                continue

            xx = four_ways(row, col, height, width)
            for (lx, ly), (rx, ry) in its.combinations(xx, 2):
                if maze[lx][ly] != "#" and maze[rx][ry] != "#":
                    savings[(row, col)] = max(savings[(row, col)], the_dist - (dist_from_start[(lx, ly)] + dist_to_end[(rx, ry)] + 1))
                    savings[(row, col)] = max(savings[(row, col)], the_dist - (dist_to_end[(lx, ly)] + dist_from_start[(rx, ry)] + 1))

    return sum(1 for val in savings.values() if val >= 100)
