function notdecreasing(s)
    s[1] <= s[2] <= s[3] <= s[4] <= s[5] <= s[6]
end

function adjacentsame(s)
    for i=1:5
        if s[i] == s[i+1]
            return true
        end
    end
    false
end

function validpassword(password)
    s = string(password)
    notdecreasing(s) && adjacentsame(s)
end

puzzle_range = 168630:718098

println(sum(map(validpassword, puzzle_range)))

function singleduplet(s)
    for i=1:5
        if s[i] == s[i+1]
            if (i > 1) && (s[i-1] == s[i])
                continue
            end
            if (i < 5) && (s[i+1] == s[i+2])
                continue
            end
            return true
        end
    end
    false
end

function validpassword2(password)
    s = string(password)
    notdecreasing(s) && adjacentsame(s) && singleduplet(s)
end

println(sum(map(validpassword2, puzzle_range)))

