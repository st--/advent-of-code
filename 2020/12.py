import numpy as np
s="""
F10
N3
F7
R90
F11
"""
s=open("12.txt").read()

lon = 0
lat = 0
hdg = 90
for line in s.split():
    action = line[0]
    arg = int(line[1:].strip())
    if action == 'N':
        lat += arg
    elif action == 'S':
        lat -= arg
    elif action == 'E':
        lon += arg
    elif action == 'W':
        lon -= arg
    elif action == 'L':
        hdg -= arg
    elif action == 'R':
        hdg += arg
    elif action == 'F':
        d_lon = np.sin(np.pi * hdg / 180) * arg
        d_lat = np.cos(np.pi * hdg / 180) * arg
        lon += d_lon
        lat += d_lat
    print(f"Current loc: {lat} N, {lon} E, heading {hdg}")
dist = np.abs(lon) + np.abs(lat)
print(f"Distance: {dist}")

lon = 0 # E
lat = 0 # N
wptlon = 10 # E
wptlat = 1 # N
for line in s.split():
    action = line[0]
    arg = int(line[1:].strip())
    if action == 'N':
        wptlat += arg
    elif action == 'S':
        wptlat -= arg
    elif action == 'E':
        wptlon += arg
    elif action == 'W':
        wptlon -= arg
    elif action in ('L', 'R'):
        dist = np.sqrt(wptlon**2 + wptlat**2)
        hdg = np.arctan2(wptlon, wptlat)
        rad = np.pi * arg / 180
        if action == 'L':
            hdg -= rad
        else:
            hdg += rad
        wptlon = np.sin(hdg) * dist
        wptlat = np.cos(hdg) * dist
    elif action == 'R':
        hdg += arg
    elif action == 'F':
        lon += arg * wptlon
        lat += arg * wptlat
    print(f"Current loc: {lat:.1f} N, {lon:.1f} E, wpt {wptlat:.1f} N, {wptlon:.1f} E of ship")
dist = np.abs(lon) + np.abs(lat)
print(f"Distance: {dist:.1f}")
