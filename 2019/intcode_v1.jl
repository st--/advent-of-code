function parse_data(program_str)
    [parse(Int64, v) for v in split(program_str, ',')]
end

function get_data()
    program_str = "1,9,10,3,2,3,11,0,99,30,40,50"
    parse_data(program_str)
end

function op_add!(program, pos)
    pos_arg1, pos_arg2, pos_result = program[pos+1:pos+3]
    program[pos_result+1] = program[pos_arg1+1] + program[pos_arg2+1]
end

function op_mul!(program, pos)
    pos_arg1, pos_arg2, pos_result = program[pos+1:pos+3]
    program[pos_result+1] = program[pos_arg1+1] * program[pos_arg2+1]
end

function op_input!(program, pos)
    pos_arg = program[pos+1]
    input = parse(Int64, readline())
    program[pos_arg+1] = input
end

function op_output!(program, pos)
    pos_arg = program[pos+1]
    output = program[pos_arg+1]
    println(output)
end

function run_opcode!(program, pos)
    opcode = program[pos]
    if opcode == 1
        op_add!(program, pos)
    elseif opcode == 2
        op_mul!(program, pos)
    elseif opcode == 3
        op_input!(program, pos)
    elseif opcode == 4
        op_output!(program, pos)
    elseif opcode == 99
        return opcode
    else
        error("unknown opcode " * string(opcode) * "!")
    end
    opcode
end

function run_program!(program)
    pos = 1
    while true
        opcode = run_opcode!(program, pos)
        if opcode == 99
            return program
        end
        pos += 4
    end
end
