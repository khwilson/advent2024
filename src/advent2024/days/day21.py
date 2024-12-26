import itertools as its
from functools import cache
from pathlib import Path

import networkx as nx


def read_data(data_file: str | Path) -> list[str]:
    with open(data_file, "rt") as infile:
        return [line.strip() for line in infile]


# Need to figure out what the right order is for the ones
# where there's more than one choice
#
# Found by just trying all the possibilities
shortest_paths = {
    "AA": "A",
    "A^": "<A",
    "A>": "vA",
    "Av": "<vA",
    "A<": "v<<A",
    "^A": ">A",
    "^^": "A",
    "^>": "v>A",
    "^v": "vA",
    "^<": "v<A",
    ">A": "^A",
    ">^": "<^A",
    ">>": "A",
    ">v": "<A",
    "><": "<<A",
    "vA": "^>A",
    "v^": "^A",
    "v>": ">A",
    "vv": "A",
    "v<": "<A",
    "<A": ">>^A",
    "<^": ">^A",
    "<>": ">>A",
    "<v": ">A",
    "<<": "A",
}


@cache
def shortest_path(x: str, y: str, depth: int) -> int:
    if depth == 1:
        return len(shortest_paths[f"{x}{y}"])

    return sum(
        shortest_path(xx, yy, depth - 1)
        for xx, yy in zip("A" + shortest_paths[f"{x}{y}"], shortest_paths[f"{x}{y}"])
    )


def part1(data_file: str | Path) -> int | str:
    return part2(data_file, is_part_one=True)


def part2(data_file: str | Path, is_part_one: bool = False) -> int | str:
    n_adj_graph = {
        "0": {"2": "^", "A": ">"},
        "A": {"0": "<", "3": "^"},
        "1": {"2": ">", "4": "^"},
        "2": {"1": "<", "3": ">", "5": "^", "0": "v"},
        "3": {"2": "<", "A": "v", "6": "^"},
        "4": {"1": "v", "5": ">", "7": "^"},
        "5": {"2": "v", "8": "^", "4": "<", "6": ">"},
        "6": {"5": "<", "9": "^", "3": "v"},
        "7": {"4": "v", "8": ">"},
        "8": {"7": "<", "5": "v", "9": ">"},
        "9": {"8": "<", "6": "v"},
    }
    n_graph = nx.Graph()
    n_graph.add_nodes_from(n_adj_graph)
    for from_key, vals in n_adj_graph.items():
        for to_key in vals:
            n_graph.add_edge(from_key, to_key)

    data = read_data(data_file)
    totals = []
    for init_code in data:
        code = f"A{init_code}A"
        all_paths = [
            [
                "".join(n_adj_graph[pp][qq] for pp, qq in zip(path, path[1:]))
                for path in nx.all_shortest_paths(n_graph, p, q)
            ]
            for p, q in zip(code, code[1:])
        ]
        all_strs = ["A".join(prod) for prod in its.product(*all_paths)]
        this_total = []
        for ss in all_strs:
            this_total.append(
                sum(
                    shortest_path(x, y, 2 if is_part_one else 25)
                    for x, y in zip("A" + ss, ss)
                )
            )

        totals.append(min(this_total) * int(init_code[:-1]))

    return sum(totals)
