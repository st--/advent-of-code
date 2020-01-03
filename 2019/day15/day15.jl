include("../intcode.jl")

tape = Tape(parse_data(readline(open("input.txt"))))

const NORTH = 1
const SOUTH = 2
const WEST = 3
const EAST = 4

const dirs = Dict(
    NORTH => [0, +1],
    SOUTH => [0, -1],
    WEST => [-1, 0],
    EAST => [+1, 0],
)

const UNEXPLORED = -1
const WALL = 0
const EMPTY = 1
const OXYGEN = 2

const chars = Dict(
    UNEXPLORED => ' ',
    WALL => '#',
    EMPTY => '.',
    OXYGEN => 'x',
)

function squeeze_map(areamap, pos)
    is_explored = areamap .!= UNEXPLORED
    exploredX = (1:size(areamap, 1))[maximum(is_explored, dims=2)[:]]
    exploredY = (1:size(areamap, 2))[maximum(is_explored, dims=1)[:]]
    lowX, hiX = minimum(exploredX), maximum(exploredX)
    lowY, hiY = minimum(exploredY), maximum(exploredY)
    shifted_pos = pos - [lowX-1, lowY-1]
    areamap[lowX:hiX, lowY:hiY], shifted_pos
end

function plot_map(areamap, pos)
    for y=size(areamap, 2):-1:1
        for x=1:size(areamap, 1)
            if [x, y] == pos
                ch = (areamap[x, y] == OXYGEN) ? '@' : 'O'
            else
                ch = chars[areamap[x, y]]
            end
            print(ch)
        end
        println()
    end
end

function read_dir()
    valid_input = map(string, collect(keys(dirs)))
    while !((input = readline()) in valid_input) end
    parse(Int, input)
end

function steer!(tape)
    areamap = fill(-1, 1001, 1001)
    pos = [501, 501]
    areamap[pos...] = 1
    while true
        out = take!(tape.outch)
        if isa(out, AwaitingInput)
            print("Direction (N=1, S=2, W=3, E=4): ")
            direction = read_dir()
            put!(tape.inch, direction)
            output = take!(tape.outch)
            dir_vec = dirs[direction]
            newpos = pos + dir_vec
            areamap[newpos...] = output
            if output != WALL
                pos = newpos
            end

            plot_map(squeeze_map(areamap, pos)...)

        elseif isa(out, CodeFinished)
            println("FINISHED")
            return
        else
            println("OUTPUT: ", out)
        end
    end
end
