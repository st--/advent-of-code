### A Pluto.jl notebook ###
# v0.12.17

using Markdown
using InteractiveUtils

# ╔═╡ db064048-3ec4-11eb-36a6-2de2e93c3b98
mutable struct State
	step
	spoken
	last
end

# ╔═╡ 21d25d36-3ec5-11eb-123c-6179223a23c9
function speak(state, num)
	state.step += 1
	state.spoken[state.last] = state.step - 1
	state.last = num
end

# ╔═╡ 49925646-3ec5-11eb-20a0-8dc9eb4f160d
function nextnum(state)
	if !(state.last in keys(state.spoken))
		return 0
	else
		return state.step - state.spoken[state.last]
	end
end	

# ╔═╡ 308d4de0-3ec5-11eb-0556-813bef55256d
function runit(starting, steps; return_history=true)
	history = []
	state = State(0, Dict(), -1)
	for n in starting
		speak(state, n)
		return_history && push!(history, n)
	end
	for i=length(starting)+1:steps
		n = nextnum(state)
		speak(state, n)
		return_history && push!(history, n)
	end
	if return_history
		history
	else
		state.last
	end
end

# ╔═╡ 223129f8-3ee6-11eb-0711-f5b9c5b005ae
starting = [7,14,0,17,11,1,2]

# ╔═╡ 1b4b07d0-3ee6-11eb-0550-69e3dcfc6914
runit(starting, 2020)[end]

# ╔═╡ f6e372ec-3ee5-11eb-2406-31cda672cc86
runit(starting, 30000000, return_history=false)

# ╔═╡ Cell order:
# ╠═db064048-3ec4-11eb-36a6-2de2e93c3b98
# ╠═21d25d36-3ec5-11eb-123c-6179223a23c9
# ╠═49925646-3ec5-11eb-20a0-8dc9eb4f160d
# ╠═308d4de0-3ec5-11eb-0556-813bef55256d
# ╠═223129f8-3ee6-11eb-0711-f5b9c5b005ae
# ╠═1b4b07d0-3ee6-11eb-0550-69e3dcfc6914
# ╠═f6e372ec-3ee5-11eb-2406-31cda672cc86
