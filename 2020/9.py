import numpy as np
dat = [int(x) for x in open("9.txt").read().strip().split()]

"""
a1+a2, a1+a3, ..., a1+a25
       a2+a3, ..., a2+a25
          a23+a24, a23+a25
                   a24+a25

       a2+a3, ..., a2+a25, a2+a26
          a23+a24, a23+a25, a23+a26
                   a24+a25, a24+a26
                            a25+a26
"""

def preamble_pairsums(lst, psize):
    p = lst[:psize]
    sums = np.full((psize, psize), np.nan)
    for i in range(psize):
        for j in range(i+1, psize):
            sums[i, j] = p[i] + p[j]
    return sums

def update_pairsums(lst, sums, offset):
    psize = sums.shape[1]
    sums[:-1, :-1] = sums[1:, 1:]
    sums[:-1, -1] = np.array(lst)[offset:offset+psize-1] + lst[offset+psize-1]
    return sums

def check(lst, psize):
    sums = preamble_pairsums(lst, psize)
    for i in range(psize, len(lst)):
        valid_set = set(sums[np.triu_indices(psize, 1)])
        if lst[i] not in valid_set:
            return lst[i]
            break
        offset = i - psize + 1
        sums = update_pairsums(lst, sums, offset)

part1_target = check(dat, 25)
print(part1_target)

for first in range(len(dat)):
    i = first
    partialsum = dat[i]
    while partialsum < part1_target:
        i += 1
        partialsum += dat[i]
    if partialsum == part1_target:
        break

contiguous = dat[first:i+1]
print(min(contiguous) + max(contiguous))
