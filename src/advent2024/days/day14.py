import itertools as its
import re
from pathlib import Path

from tqdm.auto import tqdm

MAX_X = 101
MAX_Y = 103


def read_data(data_file: str | Path) -> list[tuple[int, int, int, int]]:
    out: list[tuple[int, int, int, int]] = []
    with open(data_file, "rt") as infile:
        for line in infile:
            px, py, vx, vy = map(int, re.findall(r"([+-]?\d+)", line))
            out.append((px, py, vx, vy))

    return out


def part1(data_file: str | Path) -> int | str:
    data = read_data(data_file)
    quadrants = {0: 0, 1: 0, 2: 0, 3: 0}
    for px, py, vx, vy in data:
        end_x, end_y = (px + vx * 100) % MAX_X, (py + vy * 100) % MAX_Y
        if end_x < 50:
            if end_y < 51:
                quadrants[0] += 1
            elif end_y > 51:
                quadrants[1] += 1
        elif end_x > 50:
            if end_y < 51:
                quadrants[2] += 1
            elif end_y > 51:
                quadrants[3] += 1

    val = 1
    for v in quadrants.values():
        val *= v
    return val


def part2(data_file: str | Path) -> int | str:
    data = read_data(data_file)
    for round in tqdm(range(10_000)):
        new_data = []
        new_spots = set()
        for px, py, vx, vy in data:
            end_x, end_y = (px + vx) % MAX_X, (py + vy) % MAX_Y
            new_data.append((end_x, end_y, vx, vy))
            new_spots.add((px, py))

        # Don't know that "Christmas tree" looks like (e.g., is it just
        # an outline? is it filled in?). But in any case, a large portion
        # of the points should be within one (potentially diagonal)
        # square of the others. I tried several cutoffs in the proportion
        # but 0.7 seemed to get the right proportion
        #
        # Took around 50s to run. Almost certainly better ways to do this
        is_one_away: set[tuple[int, int]] = set()
        for (ax, ay), (bx, by) in its.combinations(new_spots, 2):
            if abs(ax - bx) + abs(ay - by) <= 2:
                is_one_away.add((ax, ay))
                is_one_away.add((bx, by))

        if len(is_one_away) / len(new_spots) > 0.7:
            print(f"Round {round}: --------------------------------")

            for i in range(MAX_X):
                for j in range(MAX_Y):
                    print("#" if (i, j) in new_spots else " ", end="")
                print()
            break

    return round
