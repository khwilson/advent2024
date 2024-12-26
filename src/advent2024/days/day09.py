import heapq
from collections import defaultdict
from pathlib import Path


def read_data(data_file: str | Path) -> list[int]:
    with open(data_file, "rt") as infile:
        return list(map(int, infile.read().strip()))


def part1(data_file: str | Path) -> int | str:
    data = read_data(data_file)

    # Don't try to do the full RLE, just have a pointer walking
    # forward and a pointer walking backward

    front_ptr = (0, 0)
    back_ptr = len(data) - 1
    if back_ptr % 2 == 1:
        # last non free block should be even
        back_ptr -= 1

    back_ptr = (back_ptr, data[back_ptr])

    checksum = 0
    pos = 0
    while True:
        if front_ptr[0] % 2 == 1:
            # We're doing free space
            checksum += (back_ptr[0] // 2) * pos
            back_ptr = (back_ptr[0], back_ptr[1] - 1)
            while back_ptr[1] == 0:
                back_ptr = (back_ptr[0] - 2, data[back_ptr[0] - 2])

        else:
            # We're doing taken space
            checksum += (front_ptr[0] // 2) * pos

        pos += 1
        front_ptr = (front_ptr[0], front_ptr[1] + 1)
        while front_ptr[1] == data[front_ptr[0]]:
            front_ptr = (front_ptr[0] + 1, 0)

        if front_ptr == back_ptr:
            break

    return checksum


def part2(data_file: str | Path) -> int | str:
    data = read_data(data_file)
    files: list[int] = []
    frees: list[int] = []
    file_pos: list[int] = []
    free_pos: list[int] = []

    # Files can be at most 9 long
    length_to_free: list[list[int]] = [[] for _ in range(10)]
    pos = 0
    for i, val in enumerate(data):
        if i % 2 == 0:
            files.append(val)
            file_pos.append(pos)
            pos += val
        else:
            frees.append(val)
            length_to_free[val].append(i // 2)
            free_pos.append(pos)
            pos += val

    # Heapify the lists so we can rearrange
    for val in length_to_free:
        heapq.heapify(val)

    back_ptr = len(files) - 1
    checksum = 0

    while back_ptr >= 0:
        file_len = files[back_ptr]
        potential_locations = []
        for length in range(file_len, 10):
            if length_to_free[length] and length_to_free[length][0] < back_ptr:
                potential_locations.append(length_to_free[length][0])
        if potential_locations:
            # Handle case when file moves
            potential_locations.sort()
            new_loc = potential_locations[0]

            # Move the file
            file_pos[back_ptr] = free_pos[new_loc]

            # Fix up our trackers
            heapq.heappop(length_to_free[frees[new_loc]])
            frees[new_loc] -= file_len
            heapq.heappush(length_to_free[frees[new_loc]], new_loc)
            free_pos[new_loc] += file_len

        checksum += back_ptr * sum(
            file_pos[back_ptr] + i for i in range(files[back_ptr])
        )
        back_ptr -= 1

    return checksum
