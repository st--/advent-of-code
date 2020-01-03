from collections import defaultdict
import numpy as np

lines = """.#....#####...#..
##...##.#####..##
##...#...#.#####.
..#.....X...###..
..#.#.....#....##""".splitlines()
lines = open('input.txt').readlines()
full_data = np.array([np.array(list(s.strip())) for s in lines])
data = (full_data == '#')

ast_seen = np.zeros(data.shape, int)

num_asteroids = data.sum()
ast_y, ast_x = np.where(data)
ast_pos = np.c_[ast_x, ast_y]
print(ast_pos.min(0), ast_pos.max(0))

best_ast = 214

x, y = center = ast_pos[best_ast]
ast_pos = np.delete(ast_pos, best_ast, axis=0)

#x, y = center = np.r_[8, 3]

idx = np.arange(len(ast_pos))

diff = ast_pos - center
diff[:, 1] = - diff[:, 1]
dist = (diff ** 2).sum(axis=1)
angle = (np.arctan2(diff[:,0], diff[:,1]) + 2 * np.pi) % (2 * np.pi)

def isapproxin(val, dct):
    if val in dct:
        return True
    for key in dct:
        if np.isclose(key, val, atol=1e-10, rtol=1e-10):
            return True
    return False

angle_dist = {}

for a, d, i in sorted(list(zip(angle, dist, idx))):
    while isapproxin(a, angle_dist):
        a += 2 * np.pi
    angle_dist[a] = i

import matplotlib.pyplot as plt
import matplotlib.cm as cm
plt.ion()

print(x, y)
plt.xlim(0, data.shape[1])
plt.ylim(0, data.shape[0])
#plt.plot(ast_pos[:,0], data.shape[0] - ast_pos[:,1], 'ko')
for c, a in enumerate(sorted(angle_dist.keys())):
    zo = 10 - int(np.ceil(c / (2 * np.pi)))
    i = angle_dist[a]
    print(c, ast_pos[i])
    ax, ay = ast_pos[i]
    plt.plot([x, ax], [data.shape[0] - y, data.shape[0] - ay],
             c=cm.jet(c/len(ast_pos)), zorder=zo)
input()

