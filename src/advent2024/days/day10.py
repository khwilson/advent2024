from pathlib import Path

import networkx as nx


def read_data(data_file: str | Path) -> list[int]:
    with open(data_file, "rt") as infile:
        return [[int(x) for x in line.strip()] for line in infile]


def four_ways(x: int, y: int, max_x: int, max_y: int) -> list[tuple[int]]:
    out = []
    for i, j in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        out.append(((x + i), (y + j)))
    out = [
        (xx, yy) for xx, yy in out if xx >= 0 and xx < max_x and yy >= 0 and yy < max_y
    ]
    return out


def part1(data_file: str | Path, is_part2: bool = False) -> int | str:
    # Today we're doing the slow thing and using a library!
    data = read_data(data_file)

    num_rows = len(data)
    num_cols = len(data[0])

    g = nx.DiGraph()
    g.add_nodes_from((i, j) for i in range(num_rows) for j in range(num_cols))

    for i in range(num_rows):
        for j in range(num_cols):
            for ii, jj in four_ways(i, j, num_rows, num_cols):
                if data[ii][jj] == data[i][j] + 1:
                    g.add_edge((i, j), (ii, jj))

    zeros = [(i, j) for i in range(num_rows) for j in range(num_cols) if data[i][j] == 0]
    nines = [(i, j) for i in range(num_rows) for j in range(num_cols) if data[i][j] == 9]

    total = 0
    func = (lambda g, z, n: sum(1 for _ in nx.all_simple_paths(g, z, n))) if is_part2 else nx.has_path
    for zero in zeros:
        for nine in nines:
            total += func(g, zero, nine)
    return total


def part2(data_file: str | Path) -> int | str:
    return part1(data_file, is_part2=True)
