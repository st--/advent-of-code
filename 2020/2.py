def parse_line(line):
    policy, password = line.split(": ")
    range_str, letter = policy.split()
    lower, upper = [int(s) for s in range_str.split("-")]
    return lower, upper, letter, password

def is_valid_1(line):
    lower, upper, letter, password = parse_line(line)
    count = password.count(letter)
    return lower <= count <= upper

def is_valid_2(line):
    first, second, letter, password = parse_line(line)
    is_first = password[first - 1] == letter
    is_second = password[second - 1] == letter
    return is_first != is_second

for is_valid in (is_valid_1, is_valid_2):
    count = 0
    with open("2.txt") as f:
        for line in f:
            if is_valid(line.strip()):
                count += 1
    print(count)
