from pathlib import Path

import numpy as np


def print_maze(maze):
    for row in maze:
        for col in row:
            print(col, end="")
        print()


def read_data(data_file: str | Path) -> tuple[list[list[str]], list[str]]:
    maze: list[list[str]] = []
    moves: list[str] = []
    with open(data_file, "rt") as infile:
        is_maze = True
        for line in infile:
            line = line.strip()
            if not line:
                is_maze = False
                continue

            if is_maze:
                maze.append([x for x in line])
            else:
                moves.extend([x for x in line])
    return maze, moves


def part1(data_file: str | Path) -> int | str:
    maze, moves = read_data(data_file)

    # Get robot position
    robot: tuple[int, int] | None = None
    for i, row in enumerate(maze):
        for j, col in enumerate(row):
            if col == "@":
                robot = (i, j)
                break
        if robot:
            break

    # Make stepping easier
    robot = np.array(list(robot))

    for move in moves:
        direction = {
            "^": np.array([-1, 0]),
            "v": np.array([1, 0]),
            "<": np.array([0, -1]),
            ">": np.array([0, 1]),
        }[move]

        # Get first free space or wall in direction
        next_pos = robot + direction
        while maze[next_pos[0]][next_pos[1]] not in ["#", "."]:
            # Works because exterior is all "#"
            next_pos += direction

        if maze[next_pos[0]][next_pos[1]] == "#":
            # Can't step in this case
            continue

        maze[robot[0]][robot[1]] = "."
        over_pos = robot + direction
        maze[over_pos[0]][over_pos[1]] = "@"
        while (over_pos != next_pos).any():
            over_pos += direction
            maze[over_pos[0]][over_pos[1]] = "O"

        robot = robot + direction

    total = 0
    for i, row in enumerate(maze):
        for j, col in enumerate(row):
            if col == "O":
                total += 100 * i + j

    return total


def part2(data_file: str | Path) -> int | str:
    data = read_data(data_file)
    return 10
