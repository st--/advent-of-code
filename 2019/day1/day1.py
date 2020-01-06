import numpy as np

def get_fuel_v1(mass):
    return int(np.floor(mass / 3) - 2)

def get_fuel_v2(mass):
    fuel = int(np.floor(mass / 3) - 2)
    if fuel <= 0:
        return 0
    else:
        return fuel + get_fuel_v2(fuel)

def load_inputs(filename):
    with open(filename) as f:
        return [int(line.strip()) for line in f]

module_masses = load_inputs("input.txt")
module_fuels = map(get_fuel_v2, module_masses)
total = sum(module_fuels)
print("Total: ", total)
