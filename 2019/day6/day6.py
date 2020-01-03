data = """COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L""".splitlines()

data = open("input.txt").read().strip().splitlines()

direct_orbit_of = {}
for line in data:
    center, satellite = line.split(')')
    direct_orbit_of[satellite] = center

all_objects = set(direct_orbit_of.keys()) | set(direct_orbit_of.values())

orbit_count_of = {'COM': 0}

def orbit_count(obj):
    if obj not in orbit_count_of:
        orbit_center = direct_orbit_of[obj]
        orbit_count_of[obj] = 1 + orbit_count(orbit_center)
    return orbit_count_of[obj]

total_orbit_count = sum(map(orbit_count, all_objects))
print(total_orbit_count)
