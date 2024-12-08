import importlib
from pathlib import Path
import time

import typer

app = typer.Typer()


@app.command()
def run(day: int, data_file: str | None = None, perf: bool = False) -> None:
    """Run an AOC day"""
    mod = importlib.import_module(f"advent2024.days.day{day:02d}")

    if not data_file:
        data_file = Path.cwd() / "data" / f"day{day:02d}.txt"

    if perf:
        totals: list[int] = []
        for _ in range(1000):
            start_time = time.perf_counter()
            mod.part1(data_file)
            end_time = time.perf_counter()
            totals.append(end_time - start_time)

        totals2: list[int] = []
        for _ in range(1000):
            start_time = time.perf_counter()
            mod.part2(data_file)
            end_time = time.perf_counter()
            totals2.append(end_time - start_time)

        print(f"Part 1: {sum(totals) / len(totals)}")
        print(f"Part 2: {sum(totals2) / len(totals2)}")

    else:
        print(f"Part 1: {mod.part1(data_file)}")
        print(f"Part 2: {mod.part2(data_file)}")


if __name__ == "__main__":
    app()
