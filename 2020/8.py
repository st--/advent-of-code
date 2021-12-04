import numpy as np
import enum

instr_ex = """
nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6
"""

@enum.unique
class Op(enum.Enum):
    acc = "acc"
    jmp = "jmp"
    nop = "nop"

def parse(s):
    ops = []
    for line in s.strip().splitlines():
        s_op, s_arg = line.split()
        op = Op(s_op)
        arg = int(s_arg)
        ops.append((op, arg))
    return ops

ops_ex = parse(instr_ex)

def nop_jmp_swap(op):
    if op == Op.nop:
        op = Op.jmp
    elif op == Op.jmp:
        op = Op.nop
    return op

def next_i(i, op, arg, swap_nop_jmp=False):
    if swap_nop_jmp:
        op = nop_jmp_swap(op)
    if op in (Op.nop, Op.acc):
        return i + 1
    elif op == Op.jmp:
        return i + arg

class RunRepeated(Exception):
    pass

class RunTerminated(Exception):
    pass

def run_oplist(ops):
    runcount = np.zeros(len(ops))
    i = 0
    acc = 0
    while not runcount[i]:
        op, arg = ops[i]
        runcount[i] += 1
        if op == Op.nop:
            i += 1
        elif op == Op.jmp:
            i += arg
        elif op == Op.acc:
            acc += arg
            i += 1
        if i >= len(ops):
            raise RunTerminated(acc)
    return acc, runcount

ops = parse(open("8.txt").read())
acc, ran = run_oplist(ops)

print(acc)

potential_swaps = []
for i in range(len(ran)):
     if not ran[i]: continue
     i2 = next_i(i, *ops[i])
     i2s = next_i(i, *ops[i], swap_nop_jmp=True)
     assert ran[i2]
     if not ran[i2s]: potential_swaps.append(i)

def swapop(ops, i):
    op, arg = ops[i]
    ops[i] = (nop_jmp_swap(op), arg)

for swap in potential_swaps:
    swapop(ops, swap)
    try:
        _ = run_oplist(ops)
    except RunTerminated as e:
        print("terminated:", e)
    swapop(ops, swap)

