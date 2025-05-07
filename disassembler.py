import sys

op_codes = {
    "000001": "R-type",
    "100100": "grab",
    "101100": "save",
    "000110": "when",
    "000111": "skip",
    "001001": "bump",
    "000000": "R-type",
    "111111": "dom",
    "101101": "maro",
    "111000": "ucl",
    "110011": "rmd",
    "100001": "egp",
    "001100": "fcb",
    "010101": "int",
    "010010": "lfc",
}

func_codes = {
    "100000": "sum",
    "100010": "dif",
    "100100": "conj",
    "100101": "disj",
    "101010": "less",
    "000000": "pwr",
    "100001": "log",
}

registers = {
    "00000": "$zero",
    "01000": "$t0",
    "01001": "$t1",
    "01010": "$t2",
    "01011": "$t3",
    "01100": "$t4",
    "01101": "$t5",
    "01110": "$t6",
    "01111": "$t7",
    "10000": "$s0",
    "10001": "$s1",
    "10010": "$s2",
    "10011": "$s3",
    "10100": "$s4",
    "10101": "$s5",
    "10110": "$s6",
    "10111": "$s7",
}

def handle_lines(bin_file: str, output_file: str = "DisassemblerOutput.asm"):
    with open(bin_file, "r") as input_file:
        line = input_file.readline().strip()
    
    mips_instructions = bin_to_mips(line)
    
    with open(output_file, "w") as output_file:
        for instruction in mips_instructions:
            output_file.write(instruction + "\n")
    
    return mips_instructions

def bin_to_mips(line):
    mips = []
    bit_string = ""
    
    for i in range(len(line)):
        bit_string += line[i]
        if len(bit_string) == 32:
            op_code = bit_string[0:6]
            
            if op_code == "000000" or op_code == "000001":
                rs, rt, rd, shift, func_code = (
                    bit_string[6:11],
                    bit_string[11:16],
                    bit_string[16:21],
                    bit_string[21:26],
                    bit_string[26:32],
                )
                
                if func_code in func_codes:
                    instr = func_codes[func_code]
                    mips.append(f"{instr} {registers[rd]}, {registers[rs]}, {registers[rt]}")
                else:
                    mips.append(f"UNKNOWN_FUNC {op_code} {func_code}")
            
            elif op_code in ["100100", "101100"]:
                rs, rt, offset = bit_string[6:11], bit_string[11:16], bit_string[16:32]
                instr = op_codes.get(op_code, "UNKNOWN")
                mips.append(f"{instr} {registers[rt]}, {int(offset, 2)}({registers[rs]})")
            
            elif op_code in ["000110", "000111"]:
                rs, rt, offset = bit_string[6:11], bit_string[11:16], bit_string[16:32]
                instr = op_codes.get(op_code, "UNKNOWN")
                mips.append(f"{instr} {registers[rs]}, {registers[rt]}, {int(offset, 2)}")
            
            elif op_code == "001001":
                rs, rt, imm = bit_string[6:11], bit_string[11:16], bit_string[16:32]
                instr = op_codes.get(op_code, "UNKNOWN")
                mips.append(f"{instr} {registers[rt]}, {registers[rs]}, {int(imm, 2)}")
            
            elif op_code in op_codes:
                instr = op_codes[op_code]
                if instr in {"dom", "maro", "ucl", "rmd", "egp", "fcb", "int", "lfc"}:
                    mips.append(instr)
                else:
                    mips.append(f"UNKNOWN_OP {op_code}")
            else:
                mips.append(f"UNKNOWN_OP {op_code}")
            
            bit_string = ""
    
    return mips

if __name__ == "__main__":
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        output_file = "DisassemblerOutput.asm"
        if len(sys.argv) > 2:
            output_file = sys.argv[2]
        handle_lines(input_file, output_file)
    else:
        handle_lines("DisassemblerInput.bin")