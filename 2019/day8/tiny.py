import numpy as np

n_cols, n_rows = 25, 6
x = np.array(list(open('input.txt').read().strip())).astype(int).reshape(-1, n_rows, n_cols)

idx_least_zero = (x == 0).sum(1).sum(1).argmin()
layer = x[idx_least_zero]
print((layer == 1).sum() * (layer == 2).sum())

idx_first_non_transparent_layer = (x != 2).argmax(axis=0)
for irow in range(n_rows):
    for icol in range(n_cols):
        ilayer = idx_first_non_transparent_layer[irow, icol]
        print('█' if x[ilayer, irow, icol] else ' ', end='')
    print()
