import re
import numpy as np

s_ex="""
class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12
"""

def parsefields(line):
    return [int(x) for x in line.split(",")]

def parseinput(s):
    s = s.strip()
    b_fields, b_own, b_nearby = s.split("\n\n")
    fields = []
    re_field = re.compile(r"([a-z ]+): (\d+)-(\d+) or (\d+)-(\d+)")
    for line in b_fields.splitlines():
        m = re_field.match(line)
        fieldname, *limits = m.groups()
        fields.append((fieldname, [int(x) for x in limits]))
    own = parsefields(b_own.splitlines()[1])
    nearbys = [parsefields(line) for line in b_nearby.splitlines()[1:]]
    return fields, own, nearbys

def make_validator(onelo, onehi, twolo, twohi):
    return lambda num: (onelo <= num <= onehi) or (twolo <= num <= twohi) 

def make_validators(fields):
    validators = []
    for name, limits in fields:
        validators.append(make_validator(*limits))
    return validators

def make_any_valid(validators):
    def validator(num):
        return any(v(num) for v in validators)
    return validator

s = open("16.txt").read()

fields, own, nearbys = parseinput(s)
vs = make_validators(fields)
av = make_any_valid(vs)

invalid_values = []
valid_tickets = []
for ns in nearbys:
    all_valid = True
    for n in ns:
        if not av(n):
            invalid_values.append(n)
            all_valid = False
    if all_valid:
        valid_tickets.append(ns)

print(sum(invalid_values))

valid_table = np.zeros((len(valid_tickets), len(vs), len(vs)), bool)
for i, ns in enumerate(valid_tickets):
    for j, v in enumerate(vs):
        for k, n in enumerate(ns):
            valid_table[i, j, k] = v(n)

all_valid_table = valid_table.all(axis=0).astype(int)
mapping = {}
while all_valid_table.shape != (0, 0):
    i, = np.where(all_valid_table.sum(axis=0) == 1)
    j, = np.where(all_valid_table.sum(axis=1) == 1)
    mapping[i.item()] = j.item()
    all_valid_table = np.delete(np.delete(all_valid_table, i, axis=0), j, axis=1)

