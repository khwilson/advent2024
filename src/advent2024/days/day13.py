import re
from pathlib import Path

import numpy as np
from scipy.linalg import solve

A_COST = 3
B_COST = 1


def read_data(
    data_file: str | Path, is_part_2: bool = False
) -> list[list[tuple[int, int]]]:
    data: list[list[tuple[int, int]]] = []
    with open(data_file, "rt") as infile:
        datum: list[tuple[int, int]] = []
        for i, line in enumerate(infile):
            if i % 4 == 3:
                pass
            elif i % 4 in [0, 1]:
                x, y = map(int, re.findall(r"[XY]([+-]\d+)", line))
                datum.append((x, y))
            elif i % 4 == 2:
                x, y = map(int, re.findall(r"[XY]=(\d+)", line))
                datum.append(
                    (x + is_part_2 * 10000000000000, y + is_part_2 * 10000000000000)
                )
                data.append(datum)
                datum = []
    return data


def part1(data_file: str | Path, is_part_2: bool = False) -> int | str:
    data = read_data(data_file, is_part_2=is_part_2)
    total = 0
    for (a_x, a_y), (b_x, b_y), (x_val, y_val) in data:
        lhs = np.array([[a_x, a_y], [b_x, b_y]]).T
        rhs = np.array([x_val, y_val])
        xx = solve(lhs, rhs)

        # Make sure solver did the right thing
        xx_val = xx[0] * a_x + xx[1] * b_x
        yy_val = xx[0] * a_y + xx[1] * b_y
        assert abs(xx_val - x_val) < 1e-2
        assert abs(yy_val - y_val) < 1e-2

        # Switch to integers
        xx = xx.round().astype(int)
        xx_val = xx[0] * a_x + xx[1] * b_x
        yy_val = xx[0] * a_y + xx[1] * b_y

        # Check for feasibility
        if (xx < 0).any():
            # Negative solution
            pass
        elif xx_val != x_val or yy_val != y_val:
            # Non-integer solution
            pass
        else:
            # Actually a solution!
            val = int(xx[0] * A_COST + xx[1] * B_COST)
            total += val

    return total


def part2(data_file: str | Path) -> int | str:
    return part1(data_file, is_part_2=True)
