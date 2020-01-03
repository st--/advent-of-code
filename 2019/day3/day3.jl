push!(LOAD_PATH, pwd())
using Day3_module

wire_paths = readlines("input.txt")
#wire_paths = ['R75,D30,R83,U83,L12,D49,R71,U7,L72',
#              'U62,R66,U55,R34,D71,R55,D58,R83']
#wire_paths = ['R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51',
#              'U98,R91,D20,R16,D67,R40,U7,R15,U6,R7']

function get_steps(wire_path)
    return split(wire_path, ',')
end

t0 = time()
pos_a, pos_b = [get_positions(get_steps(path)) for path in wire_paths]
crossings = intersect(Set(pos_a), Set(pos_b))

function manhattan_distance(pos)
    sum(map(abs, pos))
end

manhattan_distances = [manhattan_distance(pos) for pos in crossings]
println(minimum(manhattan_distances))

t1 = time()
println(t1 - t0)

println(minimum(indexin(crossings, pos_b) + indexin(crossings, pos_a)))

t2 = time()
println(t2 - t1)
