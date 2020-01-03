import numpy as np

wire_paths = open('input.txt').readlines()
#wire_paths = ['R75,D30,R83,U83,L12,D49,R71,U7,L72',
#              'U62,R66,U55,R34,D71,R55,D58,R83']
#wire_paths = ['R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51',
#              'U98,R91,D20,R16,D67,R40,U7,R15,U6,R7']

def get_steps(wire_path):
    steps = wire_path.strip().split(',')
    return steps

dirs = {
    'U': np.r_[0, +1],
    'D': np.r_[0, -1],
    'R': np.r_[+1, 0],
    'L': np.r_[-1, 0],
}

def get_positions(steps):
    current = np.r_[0, 0]
    pos = []
    for step in steps:
        direction = dirs[step[0]]
        distance = int(step[1:])
        for _ in range(distance):
            current += direction
            pos.append(tuple(current))
    return pos

import time
t0 = time.time()
pos_a, pos_b = [get_positions(get_steps(path)) for path in wire_paths]
crossings = set(pos_a) & set(pos_b)

manhattan_distances = np.abs(np.array(list(crossings))).sum(1)
print(manhattan_distances.min())

t1 = time.time()
print(t1 - t0)

steps_taken = []
for crossing in crossings:
    steps_a = pos_a.index(crossing) + 1
    steps_b = pos_b.index(crossing) + 1
    steps_taken.append(steps_a + steps_b)

print(np.min(steps_taken))

t2 = time.time()
print(t2 - t1)
