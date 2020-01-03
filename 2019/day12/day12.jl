mutable struct Moon
    pos
    vel
end

function Moon(pos)
    Moon(pos, zeros(Int64, 3))
end

mutable struct System
    moons
end

function apply_gravity_pair!(moon1, moon2)
end

function step!(moons)
    for i=1:length(moons)
        for j=i+1:length(moons)
            for d=1:3
                @inbounds if moons[j].pos[d] > moons[i].pos[d]
                    @inbounds moons[i].vel[d] += 1
                    @inbounds moons[j].vel[d] -= 1
                elseif moons[j].pos[d] < moons[i].pos[d]
                    @inbounds moons[i].vel[d] -= 1
                    @inbounds moons[j].vel[d] += 1
                end
            end
        end
    end
    for j=1:length(moons)
        for d=1:3
            @inbounds moons[j].pos[d] += moons[j].vel[d]
        end
    end
end

function run!(system, steps)
    for i=1:steps
        step!(system.moons)
    end
end

function total_energy(system::System)
    sum(total_energy(moon) for moon in system.moons)
end

function potential_energy(moon::Moon)
    sum(abs.(moon.pos))
end

function kinetic_energy(moon::Moon)
    sum(abs.(moon.vel))
end

function total_energy(moon::Moon)
    potential_energy(moon) * kinetic_energy(moon)
end

test_moons = [Moon([-1,0,2]), Moon([2,-10,-7]), Moon([4,-8,8]), Moon([3,5,1])]

# input for day 12:
input_system = System([
    Moon([15, -2, -6]),
    Moon([-5, -4, -11]),
    Moon([0, -6, 0]),
    Moon([5, 9, 6]),
])

