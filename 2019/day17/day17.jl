include("../intcode.jl")

tape = set_memory!(Tape(parse_data(readline(open("input.txt")))), 100000)

function ascii_interact!(tape)
    while true
        out = take!(tape.outch)
        if isa(out, AwaitingInput)
            input = readline()
            for ch in input
                put!(tape.inch, Int64(ch))
                out = take!(tape.outch)
                isa(out, AwaitingInput) || error("unexpected " * string(out))
            end
            put!(tape.inch, 10)
        elseif isa(out, CodeFinished)
            println("FINISHED")
            return
        else
            print(Char(out))
        end
    end
end

