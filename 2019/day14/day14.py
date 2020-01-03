import numpy as np

def load():
    data = """
    10 ORE => 10 A
    1 ORE => 1 B
    7 A, 1 B => 1 C
    7 A, 1 C => 1 D
    7 A, 1 D => 1 E
    7 A, 1 E => 1 FUEL"""
    data = open("input.txt").read()
    return data.strip().splitlines()

def parse_quantity(item):
    amount, name = item.strip().split()
    return name, int(amount)

def parse_reaction(reaction_str):
    reagents, product = reaction_str.split('=>')
    requirements = {}
    for reagent in reagents.split(','):
        name, amount = parse_quantity(reagent)
        requirements[name] = amount
    product_name, product_amount = parse_quantity(product)
    return product_name, (product_amount, requirements)

reactions = {}
for line in load():
    product_name, (product_amount, requirements) = parse_reaction(line)
    assert product_name not in reactions
    reactions[product_name] = (product_amount, requirements)

def initial_outstanding(fuel_required):
    fuel_given, outstanding = reactions['FUEL']
    times = int(np.ceil(fuel_required / fuel_given))
    return {reagent: times * required for (reagent, required) in outstanding.items()}

def reset(fuel=1):
    global outstanding, ore_required, available

    outstanding = initial_outstanding(fuel)

    ore_required = 0
    available = {}

def info(msg):
    #print(msg)
    pass

def step():
    global ore_required

    current_product = list(outstanding.keys())[0]  # pick arbitrary element
    assert current_product != 'ORE'
    amounts_required = outstanding.pop(current_product)  # and mark as done
    amount_available = available.get(current_product, 0)
    info(f"needed of {current_product}: {amounts_required} ({amount_available} already there)")

    if amounts_required <= amount_available:
        info(f"sufficient {current_product} available")
        available[current_product] -= amounts_required
        return

    amounts_required -= amount_available

    amounts_given, its_requirements = reactions[current_product]
    number_reactions = int(np.ceil(amounts_required / amounts_given))

    info(f"its requirements per reaction: {its_requirements} gives {amounts_given}")
    for reagent, per_reaction in its_requirements.items():
        total_reagent = number_reactions * per_reaction
        info(f"needs {total_reagent} {reagent}")
        if reagent == 'ORE':
            ore_required += total_reagent
        else:
            previously_required = outstanding.get(reagent, 0)
            outstanding[reagent] = previously_required + total_reagent

    available[current_product] = amounts_given * number_reactions - amounts_required
    info(f"now have {available[current_product]} of {current_product}")

def loop():
    global outstanding
    while outstanding:
        step()

def part1():
    reset()
    loop()
    print(ore_required)

TRILLION = 1000000000000
def part2(multiplier=10):
    global ore_required
    ore_required = 0
    # get upper limit
    fuel_guess = 1
    loops = 0
    while ore_required <= TRILLION:
        fuel_guess *= multiplier
        reset(fuel_guess); loop()
        loops += 1; print(fuel_guess)
    # now binary search
    lower_limit, upper_limit = fuel_guess // multiplier, fuel_guess
    while (upper_limit - lower_limit) > 1:
        fuel_guess = int(np.ceil((lower_limit + upper_limit) / 2))
        reset(fuel_guess); loop()
        loops += 1; print(lower_limit, fuel_guess, upper_limit)
        if ore_required < TRILLION:
            lower_limit = fuel_guess
        else:
            upper_limit = fuel_guess
    return loops
