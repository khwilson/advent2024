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

    # Files can be at most 9 long
    length_to_file: list[list[int]] = [[] for _ in range(10)]
    for i, val in enumerate(data):
        if i % 2 == 0:
            files.append(val)
            length_to_file[val].append(i // 2)
        else:
            frees.append(val)

    frees.append(0)

    # There are no length 0 files so we don't have to worry about their weirdness
    assert not length_to_file[0]

    length_to_file = [sorted(the_files) for the_files in length_to_file]

    front_ptr = 0  # Will point to free space
    pos = files[0]
    checksum = 0
    done_files: set[int] = {0}

    # Kill off 0 length files
    done_files |= set(length_to_file[0])
    length_to_file[0] = []

    while len(done_files) < len(files):
        # Double check the off by one here
        avail = frees[front_ptr]
        possible_files = []
        for l, the_files in enumerate(length_to_file):
            if l > avail:
                break
            while the_files and the_files[-1] in done_files:
                the_files.pop()
            if the_files:
                possible_files.append(the_files[-1])

        if not possible_files:
            # Progress the pointer
            front_ptr += 1
            pos += avail
            checksum += front_ptr * sum(pos + i for i in range(files[front_ptr]))
            pos += files[front_ptr]
            done_files.add(front_ptr)
        else:
            # Process the file
            possible_files.sort()
            file_id = possible_files[-1]
            checksum += file_id * sum(pos + i for i in range(files[file_id]))
            done_files.add(file_id)
            length_to_file[files[file_id]].pop()
            pos += files[file_id]
            frees[front_ptr] -= files[file_id]
            frees[file_id - 1] += frees[file_id] + files[file_id]
            frees[file_id] = 0

    return checksum