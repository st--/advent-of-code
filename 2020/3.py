import numpy as np
def loadmap(fn="3.txt"):
    with open(fn) as f:
        return np.array(list(map(list, f.read().splitlines())))

EMPTY = "."
TREE = "#"

def traverse(m, right=3, down=1):
    assert (right > 0) and (down > 0)
    nrows, ncols = m.shape
    x, y = 0, 0
    trees = 0
    assert m[y, x] == EMPTY
    while y < nrows - 1:
        x += right
        y += down
        x = x % ncols
        trees += (m[y, x] == TREE)
    return trees

slopes = [
    (1, 1),
    (3, 1),
    (5, 1),
    (7, 1),
    (1, 2),
]

m = loadmap()
all_trees = []
for right, down in slopes:
    trees = traverse(m, right, down)
    if (right, down) == (3, 1):
        print(trees)
    all_trees.append(trees)
print(np.prod(all_trees))
