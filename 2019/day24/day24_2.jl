
lines = readlines(open("input.txt"))
#lines = readlines(open("example.txt"))
data = cat([[x=='#' for x in line] for line in lines]..., dims=2)'

state = zeros(Bool, 403, 5, 5)
state[202, :, :] = copy(data)

function neighbours(state, d, i, j)
    nneigh = 0
    # up
    if i == 1
        nneigh += state[d-1, 2, 3]
    elseif (i == 4) && (j == 3)
        nneigh += sum(state[d+1, 5, 1:5])
    else
        nneigh += state[d, i-1, j]
    end
    # down
    if i == 5
        nneigh += state[d-1, 4, 3]
    elseif (i == 2) && (j == 3)
        nneigh += sum(state[d+1, 1, 1:5])
    else
        nneigh += state[d, i+1, j]
    end
    # left
    if j == 1
        nneigh += state[d-1, 3, 2]
    elseif (j == 4) && (i == 3)
        nneigh += sum(state[d+1, 1:5, 5])
    else
        nneigh += state[d, i, j-1]
    end
    # right
    if j == 5
        nneigh += state[d-1, 3, 4]
    elseif (j == 2) && (i == 3)
        nneigh += sum(state[d+1, 1:5, 1])
    else
        nneigh += state[d, i, j+1]
    end
    nneigh
end

function step!(next, state)
    for d=2:size(state, 1)-1
        for i=1:5
            for j=1:5
                if (i==3) && (j==3)
                    continue
                end
                nneigh = neighbours(state, d, i, j)
                if state[d, i, j]
                    next[d, i, j] = nneigh == 1
                else
                    next[d, i, j] = (nneigh == 1) || (nneigh == 2)
                end
            end
        end
    end
end

function run(state, nsteps)
    state = copy(state)
    next = copy(state)
    for i=1:nsteps
        step!(next, state)
        state, next = next, state
    end
    state
end
