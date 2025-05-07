import sys
import os

op_codes = {
    "sum": "000001",
    "dif": "000001",
    "conj": "000001",
    "disj": "000001",
    "less": "000001",
    "grab": "100100",
    "save": "101100",
    "when": "000110",
    "skip": "000111",
    "bump": "001001",
    
    "pwr": "000000",
    "log": "000000",
    "dom": "111111",
    "maro": "101101",
    "ucl": "111000",
    "rmd": "110011",
    "egp": "100001",
    "fcb": "001100",
    "int": "010101",
    "lfc": "010010",
}

func_codes = {
    "sum": "100000",
    "dif": "100010",
    "conj": "100100",
    "disj": "100101",
    "less": "101010",
    "pwr": "000000",
    "log": "100001",
}

registers = {
    "$zero": "00000",
    "$t0": "01000",
    "$t1": "01001",
    "$t2": "01010",
    "$t3": "01011",
    "$t4": "01100",
    "$t5": "01101",
    "$t6": "01110",
    "$t7": "01111",
    "$s0": "10000",
    "$s1": "10001",
    "$s2": "10010",
    "$s3": "10011",
    "$s4": "10100",
    "$s5": "10101",
    "$s6": "10110",
    "$s7": "10111",
}

shift_logic_amount = "00000"

def interpret_line(mips_file: str, output_file: str = "AssemblerOutput.txt"):
    input_file = open(mips_file, "r")
    output_file = open(output_file, "w")
    binary_output = ""
    
    for instruction in input_file:
        bin_instr = assemble(instruction)
        binary_output += bin_instr
    
    output_file.write(binary_output)
    output_file.close()
    input_file.close()
    return binary_output

def assemble(line):
    line = line.split("#")[0].strip()
    if not line:
        return ""

    parts = line.split()
    op_code = parts[0].lower()

    if op_code in func_codes:
        if len(parts) >= 4:
            rd = parts[1].replace(",", "")
            rs = parts[2].replace(",", "")
            rt = parts[3].replace(",", "")
            return (
                op_codes[op_code]
                + registers[rs]
                + registers[rt]
                + registers[rd]
                + shift_logic_amount
                + func_codes[op_code]
            )
        else:
            return "ERROR: Invalid instruction format for " + op_code

    elif op_code in ["grab", "save"]:
        if len(parts) >= 3:
            rt = parts[1].replace(",", "")
            offset_reg = parts[2].replace(")", "")
            offset, rs = offset_reg.split("(")
            offset_bin = bin(int(offset)).replace("0b", "").zfill(16)
            return op_codes[op_code] + registers[rs] + registers[rt] + offset_bin
        else:
            return "ERROR: Invalid instruction format for " + op_code
            
    elif op_code in ["when", "skip"]:
        if len(parts) >= 4:
            rs = parts[1].replace(",", "")
            rt = parts[2].replace(",", "")
            offset = parts[3].replace(",", "")
            offset_bin = bin(int(offset)).replace("0b", "").zfill(16)
            return op_codes[op_code] + registers[rs] + registers[rt] + offset_bin
        else:
            return "ERROR: Invalid instruction format for " + op_code
            
    elif op_code == "bump":
        if len(parts) >= 4:
            rt = parts[1].replace(",", "")
            rs = parts[2].replace(",", "")
            immediate = parts[3].replace(",", "")
            immediate_bin = bin(int(immediate)).replace("0b", "").zfill(16)
            return op_codes[op_code] + registers[rs] + registers[rt] + immediate_bin
        else:
            return "ERROR: Invalid instruction format for " + op_code

    elif op_code in op_codes:
        return op_codes[op_code] + "00000000000000000000000000"
    
    else:
        return "ERROR: Unknown instruction " + op_code

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        output_file = "AssemblerOutput.txt"
        if len(sys.argv) > 2:
            output_file = sys.argv[2]
        interpret_line(input_file, output_file)
    else:
        interpret_line("AssemblerInput.asm")