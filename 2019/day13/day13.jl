include("../intcode.jl")

tape = set_memory!(Tape(parse_data(readline(open("input.txt")))), 100000)

@async run_program!(tape)
output = []
while true
    ch = take!(tape.outch)
    if ch == CodeFinished()
        break
    end
    push!(output, ch)
end

instr = reshape(output[1:end], 3, div(length(output[1:end]), 3))

println(sum(instr[3, :].==2))

screen = transpose(reshape(instr[3, :], 41, 24))
for i=1:24
    for j=1:41
        val = screen[i,j]
        if val == 1 ch = '|' elseif val == 2 ch = '#' elseif val == 3 ch = '=' elseif val == 4 ch= 'O' else ch = ' ' end
        print(ch)
    end
    println()
end
