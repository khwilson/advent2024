from enum import StrEnum
from pathlib import Path
from typing import Counter


def read_data(
    data_file: str | Path,
) -> tuple[dict[str, str], list[tuple[str, str, str, str]]]:
    on_reg = True
    regs: dict[str, int] = {}

    # left, op, right, target
    instrs: list[tuple[str, str, str, str]] = []
    with open(data_file, "rt") as infile:
        for line in infile:
            line = line.strip()
            if line:
                if on_reg:
                    reg, val = line.strip().split(": ")
                    regs[reg] = int(val)
                else:
                    l, op, r, _, t = line.split()
                    instrs.append((l, op, r, t))
            else:
                on_reg = not on_reg

    return regs, instrs


class Op(StrEnum):
    AND = "AND"
    OR = "OR"
    XOR = "XOR"


def do(l: int, op: str, r: int) -> int:
    match op:
        case Op.AND:
            return l & r
        case Op.OR:
            return l | r
        case Op.XOR:
            return l ^ r
        case _:
            raise ValueError(f"Unexpected Op: {op}")


def run_circuit(x: int, y: int, instrs) -> int:
    regs = {f"x{i:02d}": int(bool(x & (1 << i))) for i in range(45)} | {
        f"y{i:02d}": int(bool(y & (1 << i))) for i in range(45)
    }

    target_to_input = {target: (l, op, r) for l, op, r, target in instrs}

    z_regs = {
        name
        for name in regs
        if name[0] == "z" and name[1].isdigit() and name[2].isdigit()
    }
    z_regs |= {
        name
        for name in target_to_input
        if name[0] == "z" and name[1].isdigit() and name[2].isdigit()
    }

    for z_reg in z_regs:
        stack: list[str] = [z_reg]
        while stack:
            if stack[-1] in regs:
                stack.pop()
            else:
                l, op, r = target_to_input[stack[-1]]
                if l in regs and r in regs:
                    regs[stack.pop()] = do(regs[l], op, regs[r])
                else:
                    if l not in regs:
                        stack.append(l)
                    if r not in regs:
                        stack.append(r)

    z_regs = list(reversed(sorted(z_regs)))
    return int("".join(str(regs[z_reg]) for z_reg in z_regs), 2)


def part1(data_file: str | Path) -> int | str:
    regs, instrs = read_data(data_file)

    # Make sure each register appears as exactly one target
    assert all(x == 1 for x in Counter(y[-1] for y in instrs).values())

    target_to_input = {target: (l, op, r) for l, op, r, target in instrs}

    z_regs = {
        name
        for name in regs
        if name[0] == "z" and name[1].isdigit() and name[2].isdigit()
    }
    z_regs |= {
        name
        for name in target_to_input
        if name[0] == "z" and name[1].isdigit() and name[2].isdigit()
    }

    for z_reg in z_regs:
        stack: list[str] = [z_reg]
        while stack:
            if stack[-1] in regs:
                stack.pop()
            else:
                l, op, r = target_to_input[stack[-1]]
                if l in regs and r in regs:
                    regs[stack.pop()] = do(regs[l], op, regs[r])
                else:
                    if l not in regs:
                        stack.append(l)
                    if r not in regs:
                        stack.append(r)

    z_regs = list(reversed(sorted(z_regs)))
    return int("".join(str(regs[z_reg]) for z_reg in z_regs), 2)


def part2(data_file: str | Path) -> int | str:
    regs, instrs = read_data(data_file)

    # Make sure each register appears as exactly one target
    assert all(x == 1 for x in Counter(y[-1] for y in instrs).values())

    target_to_input = {target: (l, op, r) for l, op, r, target in instrs}

    z_regs = {
        name
        for name in target_to_input
        if name[0] == "z" and name[1].isdigit() and name[2].isdigit()
    }

    # We're going to assume this is just supposed to be a standard adder circuit
    # that's reasonably well organized
    #
    # As the first check for that, zDD should xDD ⊕ yDD ⊕ cDD where cDD is the
    # carry bit.
    #
    # If this is well-organized, then we should always see xDD ⊕ yDD somewhere
    # in the ops. Check that this is the case
    max_reg = max(int(reg[1:]) for reg in regs)
    markers = {i: None for i in range(max_reg + 1)}
    for l, op, r, target in instrs:
        if l in regs and r in regs and l[1:] == r[1:] and op == Op.XOR:
            markers[int(l[1:])] = target
    assert all(markers.values())

    and_markers = {i: None for i in range(max_reg + 1)}
    for l, op, r, target in instrs:
        if l in regs and r in regs and l[1:] == r[1:] and op == Op.AND:
            and_markers[int(l[1:])] = target
    assert all(and_markers.values())

    # OK! It is! So now we have identified what should be the temporary
    # register that contains xDD ⊕ yDD. This bit should be used XORed
    # with exactly one other bit, which should be the carry bit.
    # EXCEPTION: z00 = x00 ⊕ y00 directly as there is not carry bit
    # Check if z00 = x00 ⊕ y00 in the circuit
    assert markers[0] == "z00"

    # Now carry on with the rest
    rev_markers = {val: key for key, val in markers.items() if val != "z00"}
    carries = {i: None for i in range(1, max_reg + 1)}
    bad_instrs = []
    good_instrs = []
    for l, op, r, target in instrs:
        assert not (l in rev_markers and r in rev_markers)
        if op != Op.XOR:
            # The carry bit is identified by the XOR
            continue

        if l in rev_markers:
            z_reg = f"z{rev_markers[l]:02d}"
            if target != z_reg:
                bad_instrs.append((l, op, r, target))
                good_instrs.append((l, op, r, z_reg))

                ol, oop, or_ = target_to_input[z_reg]
                bad_instrs.append((ol, oop, or_, z_reg))
                good_instrs.append((ol, oop, or_, target))

            else:
                carries[rev_markers[l]] = r
        elif r in rev_markers:
            z_reg = f"z{rev_markers[r]:02d}"

            if target != z_reg:
                bad_instrs.append((l, op, r, target))
                good_instrs.append((l, op, r, z_reg))

                ol, oop, or_ = target_to_input[z_reg]
                bad_instrs.append((ol, oop, or_, z_reg))
                good_instrs.append((ol, oop, or_, target))
            else:
                carries[rev_markers[r]] = l
        else:
            pass

    # At this point we seem to have identified 3 of the four things
    # we need to swap. So let's see where we are now
    new_instrs = [instr for instr in instrs if instr not in bad_instrs]
    new_instrs.extend(good_instrs)
    instrs = new_instrs

    # This indicates that there's something wrong at z15
    # for i in range(max_reg):
    #     if run_circuit(1 << i, 1 << i, instrs) != 1 << (i + 1):
    #         print(i)

    # Doing some sleuthing in the debugger:
    #   * z15 = tpr XOR dwp
    #   * dwp = x15 AND y15
    #   * tpr = wkm OR pwq
    #
    # In a traditional adder, that OR should be what creates the carry bit
    # so it's reasonable to guess that tpr is correct. OTOH, no AND gate should
    # go into the XOR, so that's likely wrong. Instead, it *should* be x15 XOR y15
    # Doing more sleuthing, that appears to plug into kfm
    # So it's likely we just need to swap those instructions
    bad_instrs.extend([("x15", "AND", "y15", "dwp"), ("y15", "XOR", "x15", "kfm")])
    good_instrs = [("x15", "AND", "y15", "kfm"), ("y15", "XOR", "x15", "dwp")]
    new_instrs = [instr for instr in instrs if instr not in bad_instrs]
    new_instrs.extend(good_instrs)
    instrs = new_instrs

    # And this seems to give the right answer
    return ",".join(sorted(instr[-1] for instr in bad_instrs))
