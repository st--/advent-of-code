import numpy as np

def tonum(s, one_ch, zero_ch):
    i_bin = s.replace(one_ch, "1").replace(zero_ch, "0")
    return int(i_bin, 2)

def parse(line):
    row = line[:7]
    col = line[-3:]
    irow = tonum(row, "B", "F")
    icol = tonum(col, "R", "L")
    seatid = irow * 8 + icol
    return (irow, icol, seatid)

seats = np.zeros((128, 8))
maxid = None
with open("5.txt") as f:
    for line in f:
        irow, icol, seatid = parse(line.strip())
        if maxid is None:
            maxid = seatid
        elif seatid > maxid:
            maxid = seatid
        seats[irow, icol] = 1
print(maxid)
myrow = np.where(seats.sum(1) == 7)[0].item()
mycol = np.where(seats[myrow] == 0)[0].item()
print(myrow * 8 + mycol)

