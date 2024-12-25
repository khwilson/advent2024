import heapq
from pathlib import Path


def read_data(data_file: str | Path) -> list[list[str]]:
    out: list[list[str]] = []
    with open(data_file, "rt") as infile:
        for line in infile:
            out.append([val for val in line.strip()])
    return out


dir_to_d = {
    "^": (-1, 0),
    "<": (0, -1),
    "v": (1, 0),
    ">": (0, 1),
}

turn_dirs = {
    ">": ("^", "v"),
    "<": ("^", "v"),
    "v": (">", "<"),
    "^": (">", "<"),
}


def next_step(
    pos: tuple[int, int], dir: str, height: int, width: int
) -> tuple[int, int] | None:
    x, y = pos
    dx, dy = dir_to_d[dir]
    x += dx
    y += dy
    if 0 <= x < height and 0 <= y < width:
        return (x, y)
    return None


def part1(data_file: str | Path) -> int | str:
    maze = read_data(data_file)
    start_pos: tuple[int, int] = ...
    end_pos: tuple[int, int] = ...
    height = len(maze)
    width = len(maze[0])
    for i, row in enumerate(maze):
        for j, val in enumerate(row):
            if val == "S":
                start_pos = (i, j)
            elif val == "E":
                end_pos = (i, j)

    cur_dir = ">"

    # Cost, pos, dir
    heap = [(0, start_pos, cur_dir)]
    seen = set()
    heapq.heapify(heap)
    while heap:
        cost, pos, cur_dir = heapq.heappop(heap)
        if pos == end_pos:
            return cost

        if (pos, cur_dir) in seen:
            continue

        seen.add((pos, cur_dir))

        next_pos = next_step(pos, cur_dir, height, width)
        if next_pos:
            if maze[next_pos[0]][next_pos[1]] != "#":
                heapq.heappush(heap, (cost + 1, next_pos, cur_dir))

        for turn_dir in turn_dirs[cur_dir]:
            next_pos = next_step(pos, turn_dir, height, width)
            if maze[next_pos[0]][next_pos[1]] != "#":
                heapq.heappush(heap, (cost + 1000 + 1, next_pos, turn_dir))

    raise ValueError


def part2(data_file: str | Path) -> int | str:
    maze = read_data(data_file)
    start_pos: tuple[int, int] = ...
    end_pos: tuple[int, int] = ...
    height = len(maze)
    width = len(maze[0])
    for i, row in enumerate(maze):
        for j, val in enumerate(row):
            if val == "S":
                start_pos = (i, j)
            elif val == "E":
                end_pos = (i, j)

    cur_dir = ">"

    # Cost, pos, dir, path
    heap = [(0, start_pos, cur_dir, (start_pos,))]
    seen: dict[tuple[tuple[int, int], str], int] = {}
    heapq.heapify(heap)
    min_cost: int | None = None
    on_paths: set[tuple[int, int]] = {start_pos, end_pos}
    while heap:
        cost, pos, cur_dir, path = heapq.heappop(heap)
        if min_cost is not None and cost > min_cost:
            return len(on_paths)

        if pos == end_pos:
            min_cost = cost
            on_paths |= set(path)
            continue

        if (pos, cur_dir) in seen and seen[(pos, cur_dir)] < cost:
            # If you get to a spot with a higher cost, we have to bail
            continue

        seen[(pos, cur_dir)] = cost

        next_pos = next_step(pos, cur_dir, height, width)
        if next_pos:
            if maze[next_pos[0]][next_pos[1]] != "#":
                heapq.heappush(heap, (cost + 1, next_pos, cur_dir, path + (next_pos,)))

        for turn_dir in turn_dirs[cur_dir]:
            next_pos = next_step(pos, turn_dir, height, width)
            if maze[next_pos[0]][next_pos[1]] != "#":
                heapq.heappush(
                    heap, (cost + 1000 + 1, next_pos, turn_dir, path + (next_pos,))
                )

    raise ValueError
