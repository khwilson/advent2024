import operator
from functools import reduce
from pathlib import Path


def read_data(data_file: str | Path) -> None:
    with open(data_file, "rt") as infile:
        out: list[tuple[int, list[int]]] = []
        for line in infile:
            val, l = line.strip().split(":")
            out.append((int(val), list(map(int, l.split()))))
    return out


def is_doable(val: int, nums: list[int]) -> bool:
    # Empty lists are ambiguous and don't occur
    # Base case is length 1
    if len(nums) == 1:
        return val == nums[0]

    if val % nums[-1] == 0 and is_doable(val // nums[-1], nums[:-1]):
        return True
    if val - nums[-1] >= 0 and is_doable(val - nums[-1], nums[:-1]):
        return True
    return False


def is_doable_part2(val: int, nums: list[int]) -> bool:
    # Empty lists are ambiguous and don't occur
    # Base case is length 1
    if len(nums) == 1:
        return val == nums[0]

    if val % nums[-1] == 0 and is_doable_part2(val // nums[-1], nums[:-1]):
        return True
    if val - nums[-1] >= 0 and is_doable_part2(val - nums[-1], nums[:-1]):
        return True

    # Concatenation asks if val % 10^(whatever) == nums[-1]
    # The 10^(whatever) part we'll just do with str operator and be lazy
    str_num = str(nums[-1])
    str_val = str(val)
    if len(str_val) > len(str_num) and str_val[-len(str_num) :] == str_num:
        str_val = str_val[: -len(str_num)]
        return is_doable_part2(int(str_val), nums[:-1])

    return False


def part1(data_file: str | Path) -> int | str:
    data = read_data(data_file)
    total = 0
    for val, nums in data:
        # Anything that is a product must be divisible, and
        # *probably* not everything is a product, so we can
        # save ourselves a lot of time by working right to
        # left, checking divisibility, and if it's not divisible
        # just doing a sum. Still technically 2^n in worst
        # case but let's assume the elves are being kind
        if is_doable(val, nums):
            total += val

    return total


def part2(data_file: str | Path) -> int | str:
    data = read_data(data_file)
    total = 0
    for val, nums in data:
        # Same idea as part 1, but now technically 3^n ;-)
        if is_doable_part2(val, nums):
            total += val

    return total
