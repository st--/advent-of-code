s_ex="""
939
7,13,x,x,59,x,31,19
"""

s="""
1007125
13,x,x,41,x,x,x,x,x,x,x,x,x,569,x,29,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,19,x,x,x,23,x,x,x,x,x,x,x,937,x,x,x,x,x,37,x,x,x,x,x,x,x,x,x,x,17
"""

def parse(s):
    line1, line2 = s.strip().splitlines()
    earliest = int(line1)
    buses = [int(n) for n in line2.split(",") if n != "x"]
    return earliest, buses

def find_answer(earliest, buses):
    def next_bus(bus):
        reps = earliest // bus
        closest = reps * bus
        if closest < earliest:
            closest += bus
        assert closest > earliest
        return closest

    next_buses = [(next_bus(bus), bus) for bus in buses]
    earliest_time, earliest_bus = sorted(next_buses)[0]
    waiting_time = earliest_time - earliest
    return earliest_bus * waiting_time

print(find_answer(*parse(s)))

"""
7,13,x,x,59,x,31,19
t s.t.
t % 7 == 0
(t+1) % 13 == 0
(t+4) % 59 == 0
(t+6) % 31 == 0
(t+7) % 19 == 0
"""
