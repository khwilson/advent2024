from functools import cmp_to_key, lru_cache
import itertools as its
from collections import defaultdict
from pathlib import Path
from typing import Literal

import networkx as nx


def read_data(data_file: str | Path) -> tuple[list[tuple[int, int]], list[int]]:
    with open(data_file, "rt") as infile:
        left: list[tuple[int, int]] = []
        right: list[int] = []

        on_left = True
        for line in infile:
            line = line.strip()
            if not line:
                on_left = not on_left
                continue

            if on_left:
                left.append(tuple(map(int, line.split("|"))))
            else:
                right.append(list(map(int, line.split(","))))

    return left, right


def part1(data_file: str | Path) -> int | str:
    left, right = read_data(data_file)

    # So technically for this one what we probably want to do is
    # create the transitive closure of the underlying graph and
    # use this as a comparison function. Just to get part 1 done
    # we'll just take then n^2 comparison route though
    rules = defaultdict(set)
    for l, r in left:
        rules[l].add(r)

    def cmp(l: int, r: int) -> Literal[-1, 0, 1]:
        if r in rules[l]:
            return -1
        if l in rules[r]:
            return 1
        return 0

    total = 0
    for line in right:
        for l, r in its.combinations(line, 2):
            if cmp(l, r) == 1:
                break
        else:
            total += line[len(line) // 2]
    return total


def part2(data_file: str | Path) -> int | str:
    left, right = read_data(data_file)

    # OK, I figured part 2 would ask us to do this....
    # Notably, I'm guessing that they've set this up
    # so that everything in linearly ordered....

    graph = nx.DiGraph()
    graph.add_nodes_from(x for pair in left for x in pair)
    graph.add_nodes_from(x for line in right for x in line)
    graph.add_edges_from(pair for pair in left)

    # Uhhh apparently the graph has a cycle? I really dislike when
    # AOC does a thing that is not specified in the rule set
    # top_sorted = list(nx.topological_sort(graph))
    # sort_order = {
    #     k: i
    #     for i, k in enumerate(top_sorted)
    # }

    # But it seems that that if you take the subgraph and topologically sort
    # that you end up winning
    total = 0
    for line in right:
        subgraph = graph.subgraph(line)
        top_sorted = list(nx.topological_sort(subgraph))
        total += top_sorted[len(top_sorted) // 2]

    return total - part1(data_file)
