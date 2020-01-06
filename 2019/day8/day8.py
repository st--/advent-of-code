import numpy as np

with open('input.txt') as f:
    s = f.read().strip()

n_cols, n_rows = 25, 6
layer_shape = (-1, n_rows, n_cols)
flat_shape = (-1, n_rows * n_cols)

x = np.array(list(s)).astype(int)
x = x.reshape(layer_shape)

per_layer_zero_count = (x.reshape(flat_shape) == 0).sum(1)
idx_least_zero = per_layer_zero_count.argmin()
layer = x[idx_least_zero]
count_1 = (layer == 1).sum()
count_2 = (layer == 2).sum()
print(count_1 * count_2)

non_transparent = x != 2
idx_first_non_transparent_layer = non_transparent.argmax(axis=0)

for irow in range(n_rows):
    for icol in range(n_cols):
        ilayer = idx_first_non_transparent_layer[irow, icol]
        color = x[ilayer, irow, icol]
        ch = '#' if color else ' '
        print(ch, end='')
    print()
