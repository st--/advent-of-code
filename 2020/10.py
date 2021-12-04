import numpy as np
from collections import Counter, defaultdict

s1 = """
16
10
15
5
1
11
7
19
6
12
4
"""

s2 = """
28
33
18
42
31
14
46
20
48
47
24
23
49
45
19
38
39
11
1
32
25
35
8
17
7
9
4
2
34
10
3
"""

s = open("10.txt").read()

lst=list(map(int, s.strip().split()))
final = np.max(lst)+3
arr=np.array([0] + sorted(lst) + [final])

counts = Counter(arr[1:] - arr[:-1])
print(counts[1] * counts[3])

ways_to_get = defaultdict(int)
current = 0
ways_to_get[current] = 1
def get_valid_next(jolt):
    return [j for j in arr if jolt < j <= jolt+3]

print(ways_to_get)
while current < final:
    print("current:", current, "-", ways_to_get[current], "ways here")
    for j in get_valid_next(current):
        ways_to_get[j] += ways_to_get[current]
        print("  can get", j, "-", ways_to_get[j])
    current += 1
    while ways_to_get[current] == 0:
        current += 1
