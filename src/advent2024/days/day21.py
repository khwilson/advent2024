import itertools as its
from collections import Counter
from functools import cache
from pathlib import Path

import networkx as nx


def read_data(data_file: str | Path) -> list[str]:
    with open(data_file, "rt") as infile:
        return [line.strip() for line in infile]


def part1(data_file: str | Path) -> int | str:
    return 10
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

    d_adj_graph = {
        "^": {"v": "v", "A": ">"},
        ">": {"v": "<", "A": "^"},
        "<": {"v": ">"},
        "v": {"<": "<", ">": ">", "^": "^"},
        "A": {"^": "<", ">": "v"},
    }

    d_graph = nx.Graph()
    d_graph.add_nodes_from(d_adj_graph)
    for from_key, vals in d_adj_graph.items():
        for to_key in vals:
            d_graph.add_edge(from_key, to_key)

    @cache
    def foo(a, b):
        return list(nx.all_shortest_paths(d_graph, a, b))

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

        for _ in range(3):
            print(all_strs)
            new_all_strs = []
            for code in all_strs:
                code = f"A{code}A"
                all_paths = [
                    [
                        "".join(d_adj_graph[pp][qq] for pp, qq in zip(path, path[1:]))
                        for path in foo(p, q)
                    ]
                    for p, q in zip(code, code[1:])
                ]
                new_all_strs.extend("A".join(prod) for prod in its.product(*all_paths))
            min_len = min(map(len, new_all_strs))
            all_strs = [x for x in new_all_strs if len(x) == min_len]

        totals.append((min(map(len, all_strs)) * int(init_code[:-1])))

    return sum(totals)

#
shortest_paths = {
    "AA": "A",
    "A^": "<A",
    "A>": "vA",
    "Av": "<vA",
    "A<": "<<vA",

    "^A": ">A",
    "^^": "A",
    "^>": "v>A",
    "^v": "vA",
    "^<": "v<A",

    ">A": "^A",
    ">^": "^<A",
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



def part2(data_file: str | Path) -> int | str:
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

    d_adj_graph = {
        "^": {"v": "v", "A": ">"},
        ">": {"v": "<", "A": "^"},
        "<": {"v": ">"},
        "v": {"<": "<", ">": ">", "^": "^"},
        "A": {"^": "<", ">": "v"},
    }

    d_graph = nx.Graph()
    d_graph.add_nodes_from(d_adj_graph)
    for from_key, vals in d_adj_graph.items():
        for to_key in vals:
            d_graph.add_edge(from_key, to_key)

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
        print(code, all_strs)
        this_total = []
        for ss in all_strs:
            this_total.append(sum(shortest_path(x, y, 25) for x, y in zip("A" + ss, ss)))
            print(len(ss), this_total[-1])

        totals.append(min(this_total) * int(init_code[:-1]))

    return sum(totals)

