include("../intcode.jl")

tape = Tape(parse_data(readline(open("input.txt"))))
set_memory!(tape, 100000)

function checked_input!(tape, value)
    sentinel = take!(tape.outch)
    if sentinel != AwaitingInput()
        error("unexpected output " * string(sentinel))
    end
    put!(tape.inch, value)
end

function run_robot!(tape, initial_panel_is_white=false)
    X = Y = Size = 1001
    is_panel_white = zeros(Bool, X, Y)
    is_repainted = zeros(Bool, X, Y)
    x = y = div(Size+1, 2)
    pos = [x, y]
    dir = [0, -1]
    RotR = [[0, -1] [1, 0]]
    is_panel_white[pos...] = initial_panel_is_white
    while true
        out = take!(tape.outch)
        if out == CodeFinished()
            break
        end
        (out == AwaitingInput()) || error("unexpected output " * string(out))
        put!(tape.inch, convert(Int64, is_panel_white[pos...]))
        paint_color = take!(tape.outch)
        is_panel_white[pos...] = convert(Bool, paint_color)
        is_repainted[pos...] = true
        turn_direction = take!(tape.outch)
        if turn_direction == 0
            # turn left
            dir = - RotR * dir
        elseif turn_direction == 1
            # turn right
            dir = RotR * dir
        else
            error("invalid turn direction " * string(turn_direction))
        end
        pos += dir
    end
    is_panel_white, is_repainted
end

function part1(program)
    tape = copy(program)
    @async run_program!(tape)
    _, is_repainted = run_robot!(tape)
    println(sum(is_repainted))
end

part1(tape)

function part2(program)
    tape = copy(program)
    @async run_program!(tape)
    is_panel_white, _ = run_robot!(tape, true)
    paintedX = (1:1001)[maximum(is_panel_white, dims=2)[:]]
    paintedY = (1:1001)[maximum(is_panel_white, dims=1)[:]]
    lowX, hiX = minimum(paintedX), maximum(paintedX)
    lowY, hiY = minimum(paintedY), maximum(paintedY)
    res = is_panel_white[lowX:hiX, lowY:hiY]
    for j=1:size(res, 2)
        for i=size(res, 1):-1:1
            print(res[i,j] ? '#' : ' ')
        end
        println()
    end
end

part2(tape)
