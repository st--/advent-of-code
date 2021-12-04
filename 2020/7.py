def parse_content(content, return_count=False):
    count, rest = content.split(" ", 1)
    color, end = rest.rsplit(" ", 1)
    assert end in ("bag", "bags")
    if return_count:
        return color, int(count)
    else:
        return color

def parse(fn="7.txt", return_count=False):
    dct = {}
    with open(fn) as f:
        for line in f:
            container_color, rhs = line.strip().split(" bags contain ")
            assert rhs.endswith(" bags.") or rhs.endswith(" bag.")
            if rhs.startswith("no other"):
                content = ()
            else:
                listing = rhs[:-1]  # remove trailing '.'
                contained = listing.split(", ")
                assert container_color not in dct
                content = tuple(parse_content(content, return_count=return_count) for content in contained)
            dct[container_color] = content
    return dct

containing = parse()
contains_shiny = {"shiny gold": True}
def does_contain_shiny(query):
    if query not in contains_shiny:
        does_contain = False
        for cont in containing[query]:
            if does_contain_shiny(cont):
                does_contain = True
        contains_shiny[query] = does_contain

    return contains_shiny[query]

print(sum([does_contain_shiny(k) for k in containing]) - 1)

containing_count = parse(return_count=True)
total_count = {}
def get_total_count(query):
    if query not in total_count:
        count = 1
        for (color, times) in containing_count[query]:
            count += times * get_total_count(color)
        total_count[query] = count

    return total_count[query]

print(get_total_count("shiny gold") - 1)
