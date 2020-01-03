include("../intcode.jl")

orig = set_memory!(Tape(parse_data(readline(open("input.txt")))), 100000)

function getval(x, y)
    tape = copy(orig)
    @async run_program!(tape)
    take!(tape.outch)
    put!(tape.inch, x)
    take!(tape.outch)
    put!(tape.inch, y)
    out = take!(tape.outch)
    take!(tape.outch)
    out
end

function getview(xsize, ysize, xoffset, yoffset)
    res = zeros(Int64, xsize, ysize)
    for i=1:xsize
        for j=1:ysize
            res[i,j] = getval(i-1+xoffset,j-1+yoffset)
        end
    end
    res
end

function showview(res)
    for i=1:size(res,1)
        for j=1:size(res,2)
            print(res[i,j])
        end
        println()
    end
end

res1 = getview(100, 100, 0, 0)
println(sum(res1))

