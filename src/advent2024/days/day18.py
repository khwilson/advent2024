from pathlib import Path

import networkx as nx
from tqdm.auto import tqdm

HEIGHT = 71
WIDTH = 71


def four_ways(x: int, y: int, max_x: int, max_y: int) -> list[tuple[int]]:
    out = []
    for i, j in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        out.append(((x + i), (y + j)))
    out = [
        (xx, yy) for xx, yy in out if xx >= 0 and xx < max_x and yy >= 0 and yy < max_y
    ]
    return out


def read_data(data_file: str | Path) -> list[tuple[int, int]]:
    with open(data_file, "rt") as infile:
        return [tuple(map(int, line.strip().split(","))) for line in infile]


def part1(data_file: str | Path) -> int | str:
    data = read_data(data_file)

    # Setup graph
    graph = nx.Graph()
    for i in range(HEIGHT):
        for j in range(WIDTH):
            graph.add_node((i, j))
            for ii, jj in four_ways(i, j, HEIGHT, WIDTH):
                graph.add_edge((i, j), (ii, jj))

    graph.remove_nodes_from(data[:1024])
    return nx.shortest_path_length(graph, (0, 0), (70, 70))


def part2(data_file: str | Path) -> int | str:
    # Solution: Just rerun dijkstra every time. Lazy!
    data = read_data(data_file)

    # Setup graph
    graph = nx.Graph()
    for i in range(HEIGHT):
        for j in range(WIDTH):
            graph.add_node((i, j))
            for ii, jj in four_ways(i, j, HEIGHT, WIDTH):
                graph.add_edge((i, j), (ii, jj))

    for i, node in tqdm(enumerate(data), total=len(data)):
        graph.remove_node(node)
        try:
            nx.shortest_path_length(graph, (0, 0), (70, 70))
        except nx.NetworkXNoPath:
            return f"{node[0]},{node[1]}"

    return 10
