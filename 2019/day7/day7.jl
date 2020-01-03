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

function amp_input!(tape, phase, input)
    checked_input!(tape, phase)
    checked_input!(tape, input)
end

function run_single_amp(tape, phase, input)
    memory = copy(tape)
    @async run_program!(memory)
    amp_input!(memory, phase, input)
    out = take!(memory.outch)
    (take!(memory.outch) == CodeFinished()) || error("unexpectedly still running")
    out
end

function run_sequential_amps(tape, phases)
    input = 0
    for phase in phases
        input = run_single_amp(tape, phase, input)
    end
    input
end

function amp_run!(tape, signal)
    sentinel = take!(tape.outch)
    if !(sentinel in (AwaitingInput(), CodeFinished()))
        error("unexpected output " * string(sentinel))
    end
    if sentinel == CodeFinished()
        return
    end
    put!(tape.inch, signal)
    take!(tape.outch)
end

function run_feedback_amps(tape, phases)
    amps = [copy(tape) for i=1:5]
    for (amp, phase) in zip(amps, phases)
        @async run_program!(amp)
        checked_input!(amp, phase)
    end
    out5 = 0
    while true
        out1 = amp_run!(amps[1], out5)
        (out1 == nothing) && break
        out2 = amp_run!(amps[2], out1)
        (out2 == nothing) && break
        out3 = amp_run!(amps[3], out2)
        (out3 == nothing) && break
        out4 = amp_run!(amps[4], out3)
        (out4 == nothing) && break
        res = amp_run!(amps[5], out4)
        (res == nothing) && break
        out5 = res
    end
    out5
end

using Combinatorics

function part1()
    maxout = 0
    maxphases = nothing
    for phases in permutations([0,1,2,3,4])
        output = run_sequential_amps(tape, phases)
        if output > maxout
            maxphases = phases
            maxout = output
        end
    end
    maxphases, maxout
end

function part2()
    maxout = 0
    maxphases = nothing
    for phases in permutations([5,6,7,8,9])
        output = run_feedback_amps(tape, phases)
        if output > maxout
            maxphases = phases
            maxout = output
        end
    end
    maxphases, maxout
end
