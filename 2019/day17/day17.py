import numpy as np

lines = open('output.txt').read().strip().splitlines()
data = np.stack([np.array(list(line)) for line in lines])

scaffolds = data == '#'
intersections = np.zeros_like(scaffolds)
Nx, Ny = scaffolds.shape
for i in range(1, Nx-1):
    for j in range(1, Ny-1):
        if scaffolds[i, j]:
            is_int = (scaffolds[i-1,j] and
                      scaffolds[i+1,j] and
                      scaffolds[i,j-1] and
                      scaffolds[i,j+1])
            intersections[i,j] = is_int

xs, ys = np.where(intersections)
print((xs * ys).sum())

