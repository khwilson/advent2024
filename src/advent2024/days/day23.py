from collections import defaultdict
from pathlib import Path


def read_data(data_file: str | Path) -> list[set[str]]:
    with open(data_file, "rt") as infile:
        return [frozenset(line.strip().split("-")) for line in infile]



def part1(data_file: str | Path) -> int | str:
    data = read_data(data_file)
    adj_graph: dict[str, set[str]] = defaultdict(set)
    for l, r in data:
        adj_graph[l].add(r)
        adj_graph[r].add(l)

    seen: set[frozenset[str]] = set()
    for one in adj_graph:
        if one[0] != "t":
            continue

        for two in adj_graph[one]:
            for three in adj_graph[two]:
                if one in adj_graph[three]:
                    the_set = frozenset([one, two, three])
                    seen.add(the_set)
    return len(seen)

def part2(data_file: str | Path) -> int | str:
    data = read_data(data_file)

    # OK, so they want us to do max clique. Gotta love a good NP-complete
    # problem late in time!
    return 10
