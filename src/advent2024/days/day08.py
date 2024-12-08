import itertools as its
from collections import defaultdict
from pathlib import Path


def read_data(data_file: str | Path) -> list[list[str]]:
    with open(data_file, "rt") as infile:
        return [[x for x in line.strip()] for line in infile]


def part1(data_file: str | Path, is_part2: bool = False) -> int | str:
    data = read_data(data_file)

    # Parse node positions
    nodes: dict[str, set[tuple[int, int]]] = defaultdict(set)
    for num_row, row in enumerate(data):
        for num_col, val in enumerate(row):
            if val != ".":
                nodes[val].add((num_row, num_col))

    max_row = len(data)
    max_col = len(data[0])

    antinodes: set[tuple[int, int]] = set()
    for _, positions in nodes.items():
        if is_part2 and len(positions) > 1:
            antinodes |= positions

        for (left_row, left_col), (right_row, right_col) in its.combinations(
            positions, 2
        ):
            drow = left_row - right_row
            dcol = left_col - right_col
            trow = drow
            tcol = dcol
            while True:
                do_break = 0
                arow = left_row + trow
                acol = left_col + tcol
                if 0 <= arow < max_row and 0 <= acol < max_col:
                    antinodes.add((arow, acol))
                else:
                    do_break += 1

                brow = right_row - trow
                bcol = right_col - tcol
                if 0 <= brow < max_row and 0 <= bcol < max_col:
                    antinodes.add((brow, bcol))
                else:
                    do_break += 1

                trow += drow
                tcol += dcol
                if (not is_part2) or (do_break == 2):
                    break

    return len(antinodes)


def part2(data_file: str | Path) -> int | str:
    return part1(data_file, is_part2=True)
