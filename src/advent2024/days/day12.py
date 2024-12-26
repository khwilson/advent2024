from pathlib import Path

import networkx as nx


def four_ways(x: int, y: int, max_x: int, max_y: int) -> list[tuple[int]]:
    out = []
    for i, j in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        out.append(((x + i), (y + j)))
    out = [
        (xx, yy) for xx, yy in out if xx >= 0 and xx < max_x and yy >= 0 and yy < max_y
    ]
    return out


def read_data(data_file: str | Path) -> list[list[str]]:
    out: list[list[str]] = []
    with open(data_file, "rt") as infile:
        for line in infile:
            line = line.strip()
            out.append([x for x in line])
    return out


def part1(data_file: str | Path) -> int | str:
    data = read_data(data_file)

    # To be easily able to use our standard four_way function,
    # we'll add some padding
    data = [
        ["#"] * (len(data[0]) + 2),
        *[["#"] + row + ["#"] for row in data],
        ["#"] * (len(data[0]) + 2),
    ]

    height = len(data)
    width = len(data[0])

    # Add initial nodes
    graph = nx.Graph()
    graph.add_nodes_from((i, j) for i in range(height) for j in range(width))

    for i, row in enumerate(data):
        for j, val in enumerate(row):
            for ii, jj in four_ways(i, j, height, width):
                if data[ii][jj] == val:
                    graph.add_edge((i, j), (ii, jj))

    # Sadly, we're not guaranteed things are simply connected, so we
    # can't be clever and use variants on Pick's Theorem. So we'll
    # just do it by hand
    cost = 0
    for component in nx.connected_components(graph):
        xx, yy = list(component)[0]
        val = data[xx][yy]
        if val == "#":
            # This is the padding component
            continue

        area = len(component)
        perimieter_set = set()
        for i, j in component:
            # Check the four sides of the box
            for ii, jj in four_ways(i, j, height, width):
                if (ii, jj) in component:
                    # Not on the perimeter
                    continue
                # This edge is on the perimeter. Give it a unique name
                perimieter_set.add(frozenset([(i, j), (ii, jj)]))
        cost += area * len(perimieter_set)

    return cost


def part2(data_file: str | Path) -> int | str:
    data = read_data(data_file)

    # To be easily able to use our standard four_way function,
    # we'll add some padding
    data = [
        ["#"] * (len(data[0]) + 2),
        *[["#"] + row + ["#"] for row in data],
        ["#"] * (len(data[0]) + 2),
    ]

    height = len(data)
    width = len(data[0])

    # Add initial nodes
    graph = nx.Graph()
    graph.add_nodes_from((i, j) for i in range(height) for j in range(width))

    for i, row in enumerate(data):
        for j, val in enumerate(row):
            for ii, jj in four_ways(i, j, height, width):
                if data[ii][jj] == val:
                    graph.add_edge((i, j), (ii, jj))

    # Sadly, we're not guaranteed things are simply connected, so we
    # can't be clever and use variants on Pick's Theorem. So we'll
    # just do it by hand
    cost = 0
    for component in nx.connected_components(graph):
        xx, yy = list(component)[0]
        val = data[xx][yy]
        if val == "#":
            # This is the padding component
            continue

        area = len(component)
        perimieter_set = set()
        for i, j in component:
            # Check the four sides of the box
            for ii, jj in four_ways(i, j, height, width):
                if (ii, jj) in component:
                    # Not on the perimeter
                    continue
                # This edge is on the perimeter. Give it a unique name
                perimieter_set.add(frozenset([(i, j), (ii, jj)]))

        # Get the sides; just be lazy and make another graph
        p_graph = nx.Graph()
        p_graph.add_nodes_from(perimieter_set)
        for edge in perimieter_set:
            l, r = tuple(edge)
            if l[0] == r[0]:
                # (i, j) should be the one with `val`
                i = l[0]
                j = min(l[1], r[1])
                if data[i][j] == val:
                    jj = j + 1
                else:
                    jj = j
                    j = j + 1
                above = frozenset([(i - 1, j), (i - 1, jj)])
                below = frozenset([(i + 1, j), (i + 1, jj)])
                if above in perimieter_set:
                    if data[i - 1][j] == val:
                        # Check orientation
                        p_graph.add_edge(edge, above)
                if below in perimieter_set:
                    if data[i + 1][j] == val:
                        p_graph.add_edge(edge, below)
            elif l[1] == r[1]:
                j = l[1]
                i = min(l[0], r[0])
                if data[i][j] == val:
                    ii = i + 1
                else:
                    ii = i
                    i = i + 1
                above = frozenset([(i, j - 1), (ii, j - 1)])
                below = frozenset([(i, j + 1), (ii, j + 1)])
                if above in perimieter_set:
                    if data[i][j - 1] == val:
                        p_graph.add_edge(edge, above)
                if below in perimieter_set:
                    if data[i][j + 1] == val:
                        p_graph.add_edge(edge, below)
            else:
                ValueError("Can't happen")
        num_sides = sum(1 for _ in nx.connected_components(p_graph))
        cost += area * num_sides

    return cost
