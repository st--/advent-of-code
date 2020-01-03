__precompile__()
module Day3_module

export get_positions

dirs = Dict(
    'U' => [0, +1],
    'D' => [0, -1],
    'R' => [+1, 0],
    'L' => [-1, 0],
)

function get_positions(steps)
print(typeof(steps))
    current = [0, 0]
    pos = Array{Tuple{Int64, Int64}}(undef, 0)
    for next in steps
        direction = dirs[next[1]]
        distance = parse(Int64, next[2:end])
        for i=1:distance
            current += direction
            push!(pos, tuple(current...))
        end
    end
    pos
end

precompile(get_positions, (Array{SubString{String},1},))

end
