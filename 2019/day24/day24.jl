
lines = readlines(open("input.txt"))
#lines = readlines(open("example.txt"))
data = cat([[x=='#' for x in line] for line in lines]..., dims=2)'

state = copy(data)
next = zeros(Bool, 5, 5)
nneigh = zeros(Int64, 5, 5)

function neighbours(state, i, j)
    nneigh = 0
    if i > 1 nneigh += state[i-1, j] end
    if i < 5 nneigh += state[i+1, j] end
    if j > 1 nneigh += state[i, j-1] end
    if j < 5 nneigh += state[i, j+1] end
    nneigh
end

function neighbours!(nneigh, state)
    for i=1:5
        for j=1:5
            nneigh[i, j] = neighbours(state, i, j)
        end
    end
end

function step!(next, state)
    for i=1:5
        for j=1:5
            nneigh = neighbours(state, i, j)
            if state[i, j]
                next[i, j] = nneigh == 1
            else
                next[i, j] = (nneigh == 1) || (nneigh == 2)
            end
        end
    end
end

base = [2^(i-1) for i=1:25]

function stateid(state)
    id = 0
    for i=1:25
        if state[i]
            id += base[i]
        end
    end
    id
end

function run(state)
    seen = Set{Int64}([stateid(state)])
    state = copy(state)
    next = copy(state)
    while true
        step!(next, state)
        state, next = next, state
        id = stateid(state)
        if id in seen
            break
        end
        push!(seen, id)
    end
    state
end
