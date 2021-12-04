### A Pluto.jl notebook ###
# v0.12.16

using Markdown
using InteractiveUtils

# ╔═╡ 7cbf25aa-3def-11eb-0c74-af66e15f45ca
s_ex = """mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0"""

# ╔═╡ 70c2c378-3e01-11eb-34c7-d17201765158
lines = readlines("14.txt")

# ╔═╡ 8fe5aaf2-3def-11eb-2708-d395cd38ffde
lines_ex = split(s_ex, "\n")

# ╔═╡ 0a9f638a-3dfc-11eb-3c1a-d3d4f9eab152
function maskedvalue(mask, value)
	bin_arr = lpad(string(value, base=2), 36, "0")
	masked = join([m == 'X' ? v : m for (m, v) in zip(mask, bin_arr)])
	parse(Int64, masked, base=2)
end

# ╔═╡ 40bb7a5e-3e05-11eb-046e-d9cef0009c51
function flipidx(binarr, idx, value="1")
	binarr[1:idx-1] * value * binarr[idx+1:end]
end

# ╔═╡ 7f768d70-3e04-11eb-0a0c-91bb5677385a
function maskedaddresses(mask, value)
	N = length(mask)
	bin_arr = lpad(string(value, base=2), N, "0")
	floating_bits = [i for i in 1:N if mask[i] == 'X']
	masked = join([m == '0' ? v : m for (m, v) in zip(mask, bin_arr)])
	addrs = [masked]
	for idx in floating_bits
		new_addrs = []
		for addr in addrs
			@assert addr[idx] == 'X'
			push!(new_addrs, flipidx(addr, idx, "0"))
			push!(new_addrs, flipidx(addr, idx, "1"))
		end
		addrs = new_addrs
	end
	# floating_bits, masked, addrs
	[parse(Int64, s, base=2) for s in addrs]
end

# ╔═╡ 9d343d2c-3def-11eb-155e-6ff7501e4fb6
function parseline(line, mask, memory::Dict)
	m = match(r"mask = ([X01]+)", line)
	if m !== nothing
		mask = m.captures[1]
		return mask, memory
	end
	m = match(r"mem\[([0-9]+)\] = ([0-9]+)", line)
	if m !== nothing
		mem_idx = parse(Int64, m.captures[1])
		value = parse(Int64, m.captures[2])
		memory[mem_idx] = maskedvalue(mask, value)
		return mask, memory
	end
	println("Unparsed `$(line)`")
end

# ╔═╡ fe31a3d8-3e00-11eb-3b37-cdc824855e51
begin
	mask = join("X" for i=1:36)
	memory = Dict()
	for line in lines
		mask, memory = parseline(line, mask, memory)
	end
	sum(values(memory))
end

# ╔═╡ e665342a-3e09-11eb-2e93-fb0813ae24af
function parseline2(line, mask, memory::Dict)
	m = match(r"mask = ([X01]+)", line)
	if m !== nothing
		mask = m.captures[1]
		return mask, memory
	end
	m = match(r"mem\[([0-9]+)\] = ([0-9]+)", line)
	if m !== nothing
		mem_idx = parse(Int64, m.captures[1])
		value = parse(Int64, m.captures[2])
		for addr in maskedaddresses(mask, mem_idx)
			memory[addr] = value
		end
		return mask, memory
	end
	println("Unparsed `$(line)`")
end

# ╔═╡ c0ee620a-3e09-11eb-2ded-7d1ffe2c0243
begin
	mask2 = join("X" for i=1:36)
	memory2 = Dict()
	for line in lines
		mask2, memory2 = parseline2(line, mask2, memory2)
	end
	sum(values(memory2))
end

# ╔═╡ Cell order:
# ╠═7cbf25aa-3def-11eb-0c74-af66e15f45ca
# ╠═70c2c378-3e01-11eb-34c7-d17201765158
# ╠═8fe5aaf2-3def-11eb-2708-d395cd38ffde
# ╠═0a9f638a-3dfc-11eb-3c1a-d3d4f9eab152
# ╠═40bb7a5e-3e05-11eb-046e-d9cef0009c51
# ╠═7f768d70-3e04-11eb-0a0c-91bb5677385a
# ╠═9d343d2c-3def-11eb-155e-6ff7501e4fb6
# ╠═fe31a3d8-3e00-11eb-3b37-cdc824855e51
# ╠═e665342a-3e09-11eb-2e93-fb0813ae24af
# ╠═c0ee620a-3e09-11eb-2ded-7d1ffe2c0243
