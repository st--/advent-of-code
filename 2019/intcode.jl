struct AwaitingInput end
struct CodeFinished end
const IntcodeOutput = Union{Int64, AwaitingInput, CodeFinished}

mutable struct Tape
    tape::Array{Int64,1}
    pos::Int64
    relbase::Int64
    inch::Channel{Int64}
    outch::Channel{IntcodeOutput}
end

function Tape(tape, pos, relbase)
    Tape(tape, pos, relbase, Channel{Int64}(1), Channel{IntcodeOutput}(1))
end

function Tape(tape)
    Tape(tape, 0, 0)
end

function Base.copy(tape)
    Tape(copy(tape.tape), tape.pos, tape.relbase)
end

function read(tape::Tape, pos)
    return tape.tape[pos + 1]
end

function write!(tape::Tape, pos, value)
    tape.tape[pos + 1] = value
end

const POSITION_MODE = 0
const IMMEDIATE_MODE = 1
const RELATIVE_MODE = 2

function get_op_mode(tape::Tape, offset)
    instruction = read(tape, tape.pos)
    param_mode = div(instruction, 10^(1+offset)) % 10
end

function get_arg(tape::Tape, offset)
    mode = get_op_mode(tape, offset)
    if mode == POSITION_MODE
        pos_arg = read(tape, tape.pos + offset)
        arg = read(tape, pos_arg)
    elseif mode == IMMEDIATE_MODE
        arg = read(tape, tape.pos + offset)
    elseif mode == RELATIVE_MODE
        pos_arg = read(tape, tape.pos + offset)
        arg = read(tape, tape.relbase + pos_arg)
    else
        error("invalid mode: " * mode * " !")
    end
    arg
end

function set_arg!(tape::Tape, offset, value)
    mode = get_op_mode(tape, offset)
    pos = read(tape, tape.pos + offset)
    if mode == RELATIVE_MODE
        pos += tape.relbase
    end
    write!(tape, pos, value)
end

function op_add!(tape)
    arg1 = get_arg(tape, 1)
    arg2 = get_arg(tape, 2)
    result = arg1 + arg2
    set_arg!(tape, 3, result)
    tape.pos += 4
end

function op_mul!(tape)
    arg1 = get_arg(tape, 1)
    arg2 = get_arg(tape, 2)
    result = arg1 * arg2
    set_arg!(tape, 3, result)
    tape.pos += 4
end

function op_input!(tape)
    put!(tape.outch, AwaitingInput())
    input = take!(tape.inch)
    set_arg!(tape, 1, input)
    tape.pos += 2
end

function op_output!(tape)
    output = get_arg(tape, 1)
    put!(tape.outch, output)
    tape.pos += 2
end

function op_jumptrue!(tape)
    arg1 = get_arg(tape, 1)
    arg2 = get_arg(tape, 2)
    if arg1 != 0
        tape.pos = arg2
    else
        tape.pos += 3
    end
end

function op_jumpfalse!(tape)
    arg1 = get_arg(tape, 1)
    arg2 = get_arg(tape, 2)
    if arg1 == 0
        tape.pos = arg2
    else
        tape.pos += 3
    end
end

function op_lessthan!(tape)
    arg1 = get_arg(tape, 1)
    arg2 = get_arg(tape, 2)
    set_arg!(tape, 3, arg1 < arg2 ? 1 : 0)
    tape.pos += 4
end

function op_equal!(tape)
    arg1 = get_arg(tape, 1)
    arg2 = get_arg(tape, 2)
    set_arg!(tape, 3, arg1 == arg2 ? 1 : 0)
    tape.pos += 4
end

function op_adjustrelbase!(tape)
    arg = get_arg(tape, 1)
    tape.relbase += arg
    tape.pos += 2
end

function run_opcode!(tape)
    instruction = read(tape, tape.pos)
    opcode = instruction % 100
    if opcode == 99     return opcode
    elseif opcode == 1  op_add!(tape)
    elseif opcode == 2  op_mul!(tape)
    elseif opcode == 3  op_input!(tape)
    elseif opcode == 4  op_output!(tape)
    elseif opcode == 5  op_jumptrue!(tape)
    elseif opcode == 6  op_jumpfalse!(tape)
    elseif opcode == 7  op_lessthan!(tape)
    elseif opcode == 8  op_equal!(tape)
    elseif opcode == 9  op_adjustrelbase!(tape)
    else
        error("unknown opcode " * string(opcode) * "!")
    end
    opcode
end

function run_program!(tape)
    while true
        opcode = run_opcode!(tape)
        if opcode == 99
            put!(tape.outch, CodeFinished())
            return tape
        end
    end
end

function set_memory!(tape, size)
    memory = zeros(Int64, size)
    memory[1:length(tape.tape)] = tape.tape
    tape.tape = memory
    tape
end

function interact!(tape)
    while true
        out = take!(tape.outch)
        if isa(out, AwaitingInput)
            print("INPUT: ")
            input = readline()
            put!(tape.inch, parse(Int64, input))
        elseif isa(out, CodeFinished)
            println("FINISHED")
            return
        else
            println("OUTPUT: ", out)
        end
    end
end

function parse_data(program_str)
    [parse(Int64, v) for v in split(program_str, ',')]
end
