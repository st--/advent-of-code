def parse(group):
    return len(set(group.replace("\n", "")))
groups = open("6.txt").read().split("\n\n")
print(sum(parse(g) for g in groups))
def parse2(group):
    q_yes = list(map(set, group.split()))
    return len(set.intersection(*q_yes))
print(sum(parse2(g) for g in groups))
