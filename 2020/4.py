fulltext = open("4.txt").read()
passports = fulltext.split("\n\n")
def intrange(lower, upper):
    def validator(s):
        try:
            num = int(s)
        except ValueError:
            return False
        else:
            return lower <= num <= upper
    return validator
def unitsplitter(unitdict):
    def validator(s):
        unit = s[-2:]  # HACK
        if unit not in unitdict:
            return False
        return unitdict[unit](s[:-2])
    return validator
def haircolor(s):
    if s[0] != "#" or len(s[1:]) != 6:
        return False
    try:
        _ = int(s[1:], 16)
    except ValueError:
        return False
    else:
        return True
def ninedigit(s):
    return len(s) == 9 and s.isdigit()
validators = {
    "byr": intrange(1920, 2002),
    "iyr": intrange(2010, 2020),
    "eyr": intrange(2020, 2030),
    "hgt": unitsplitter({
        "cm": intrange(150, 193),
        "in": intrange(59, 76),
        }),
    "hcl": haircolor,
    "ecl": lambda s: s in {"amb", "blu", "brn", "gry", "grn", "hzl", "oth"},
    "pid": ninedigit,
    #"cid",
}
fields = set(validators.keys())
valid = 0
for p in passports:
    keys = [kv.split(":")[0] for kv in p.split()]
    if set(keys) - {"cid"} == fields:
        valid += 1
print(valid)
valid = 0
for p in passports:
    kv = dict([kv.split(":") for kv in p.split()])
    if "cid" in kv:
        del kv["cid"]
    if set(kv.keys()) == fields:
        if all(validators[k](v) for k, v in kv.items()):
            valid += 1
print(valid)
