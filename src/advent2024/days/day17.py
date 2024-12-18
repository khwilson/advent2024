import re
from copy import copy
from enum import IntEnum
from pathlib import Path


class Inst(IntEnum):
    ADV = 0
    BXL = 1
    BST = 2
    JNZ = 3
    BXC = 4
    OUT = 5
    BDV = 6
    CDV = 7


class State:
    def __init__(
        self,
        reg_a: int,
        reg_b: int,
        reg_c: int,
        instructions: list[tuple[int, int]],
        instr_ptr: int = 0,
    ):
        self.reg_a = reg_a
        self.reg_b = reg_b
        self.reg_c = reg_c
        self.instructions = copy(instructions)
        self.instr_ptr = instr_ptr
        self.output: list[int] = []

    def __repr__(self) -> str:
        return f"<State: ({self.reg_a}, {self.reg_b}, {self.reg_c}), {self.instr_ptr}>"

    def do(self) -> bool:
        match self.instructions[self.instr_ptr]:
            case (Inst.ADV, op):
                self.reg_a = self.reg_a >> self.resolve_combo(op)
                self.instr_ptr += 1

            case (Inst.BXL, op):
                self.reg_b ^= op
                self.instr_ptr += 1

            case (Inst.BST, op):
                self.reg_b = self.resolve_combo(op) & 7
                self.instr_ptr += 1

            case (Inst.JNZ, op):
                self.instr_ptr = op // 2 if self.reg_a != 0 else self.instr_ptr + 1

            case (Inst.BXC, op):
                self.reg_b ^= self.reg_c
                self.instr_ptr += 1

            case (Inst.OUT, op):
                self.output.append(self.resolve_combo(op) & 7)
                self.instr_ptr += 1

            case (Inst.BDV, op):
                self.reg_b = self.reg_a >> self.resolve_combo(op)
                self.instr_ptr += 1

            case (Inst.CDV, op):
                self.reg_c = self.reg_a >> self.resolve_combo(op)
                self.instr_ptr += 1

            case _:
                raise ValueError("Unexpected instruction")

        # Return whether the program has halted
        return self.instr_ptr < len(self.instructions)

    def resolve_combo(self, op: int) -> int:
        if 0 <= op <= 3:
            return op
        if op == 4:
            return self.reg_a
        if op == 5:
            return self.reg_b
        if op == 6:
            return self.reg_c
        if op == 7:
            raise ValueError("op cannot be 7")


def read_data(data_file: str | Path) -> tuple[int, int, int, list[tuple[int, int]]]:
    with open(data_file, "rt") as infile:
        reg_a = int(re.findall(r"(\d+)", next(infile))[0])
        reg_b = int(re.findall(r"(\d+)", next(infile))[0])
        reg_c = int(re.findall(r"(\d+)", next(infile))[0])
        next(infile)
        raw_instr = list(map(int, next(infile).strip().split(": ")[1].split(",")))
        instructions = list(zip(raw_instr[::2], raw_instr[1::2]))

        return reg_a, reg_b, reg_c, instructions


def part1(data_file: str | Path) -> int | str:
    reg_a, reg_b, reg_c, instructions = read_data(data_file)
    state = State(reg_a, reg_b, reg_c, instructions)
    while state.do():
        pass

    return ",".join(map(str, state.output))


def part2(data_file: str | Path) -> int | str:
    # The program executes in full each time and
    # only prints the contents of register B
    #
    # To exit, register A = 0
    # Each round, register B and C both are reset
    #
    # Each round, register A is shifted right 3 bits
    #
    # So we just need to figure out what the relevant
    # last three bits of register A are. Just
    # brute force in reverse :-)
    _, _, _, instructions = read_data(data_file)
    flat_instr = [x for y in instructions for x in y]
    reg_a = 0
    for j in range(len(flat_instr)):
        for val in range(8):
            state = State((reg_a << 3) | val, 0, 0, instructions)
            while state.do():
                pass
            if state.output == flat_instr[-j - 1 :]:
                reg_a = (reg_a << 3) | val
                break

    return reg_a
