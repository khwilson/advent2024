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
    return 10
