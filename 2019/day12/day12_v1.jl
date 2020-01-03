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
    velocity_change_1 = sign.(moon2.pos - moon1.pos)
    moon1.vel += velocity_change_1
    moon2.vel -= velocity_change_1
end

function apply_gravity!(moons)
    for i=1:length(moons)
        for j=i+1:length(moons)
            apply_gravity_pair!(moons[i], moons[j])
        end
    end
end

function apply_velocity_single!(moon)
    moon.pos += moon.vel
end

function apply_velocity!(moons)
    for moon in moons
        apply_velocity_single!(moon)
    end
end

function step!(moons)
    apply_gravity!(moons)
    apply_velocity!(moons)
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

input_system = System([
    Moon([15, -2, -6]),
    Moon([-5, -4, -11]),
    Moon([0, -6, 0]),
    Moon([5, 9, 6]),
])

