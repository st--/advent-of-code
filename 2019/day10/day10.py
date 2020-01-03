import numpy as np

lines = """.#..#
.....
#####
....#
...##""".splitlines()
lines = open('input.txt').readlines()
full_data = np.array([np.array(list(s.strip())) for s in lines])
data = (full_data == '#')

ast_seen = np.zeros(data.shape, int)

num_asteroids = data.sum()
ast_x, ast_y = np.where(data)
ast_pos = np.c_[ast_x, ast_y]

def shift_multiple(this, others):
    same_quadrant = (np.sign(this) == np.sign(others)).all(axis=1)
    rel = this[None, :] / others
    is_same_rel = rel[:, 0] == rel[:, 1]
    other_not_zero_c = others != 0
    other_not_zero = other_not_zero_c[:, 0] & other_not_zero_c[:, 1]
    return same_quadrant & is_same_rel & other_not_zero

def check_axis(this, others):
    if this > 0:
        is_blocked = (others[others > 0] < this).any() and len(others) > 0
    else:
        is_blocked = (others[others < 0] > this).any() and len(others) > 0
    return is_blocked

best_seen = 0
best_ast = None
for i in range(num_asteroids):
    shifts = ast_pos - ast_pos[i]
    def sqdist(pos):
        return (pos ** 2).sum()
    shifts_by_dist = np.array(sorted(shifts, key=sqdist))
    num_seen = 0
    screen = full_data.copy()
    for j in range(num_asteroids-1, 0, -1):
        this = shifts_by_dist[j]
        others = shifts_by_dist[1:j]
        x, y = ast_pos[i] + this
        if this[0] == 0:
            mask = others[:, 0] == 0
            is_blocked = check_axis(this[1], others[mask, 1])
        elif this[1] == 0:
            mask = others[:, 1] == 0
            is_blocked = check_axis(this[0], others[mask, 0])
        else:
            is_blocked = shift_multiple(this, others).any()
        if not is_blocked:
            screen[x, y] = '*'
            num_seen += 1
        else:
            screen[x, y] = '@'
    x, y = ast_pos[i]
    screen[x, y] = 'X'
    ast_seen[x, y] = num_seen
    if num_seen > best_seen:
        best_seen = num_seen
        best_ast = i
    #print(screen)
    #print(num_seen)
    #input()

print(best_seen)
print(best_ast)
