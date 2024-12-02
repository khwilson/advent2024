from pathlib import Path

from advent2024.days import day02


def test_day02_part1(fixtures_path: Path):
    import ipdb

    ipdb.set_trace()
    assert day02.part1(fixtures_path / "day02.txt") == 10


def test_day02_part2(fixtures_path: Path):
    assert day02.part2(fixtures_path / "day02.txt") == 10
