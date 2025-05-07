import sys

op_codes = {
    "100011": "lw",
    "101011": "sw",
    "000100": "beq",
    "000101": "bne",
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
    "100000": "add",
    "100010": "sub",
    "100100": "and",
    "100101": "or",
    "101010": "slt",
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


def handle_lines(bin_file: str):
    with open(bin_file, "r") as input_file:
        line = input_file.readline().strip()
    mips_instructions = bin_to_mips(line)
    with open("DisassemblerOutput.asm", "w") as output_file:
        for instruction in mips_instructions:
            output_file.write(instruction + "\n")


def bin_to_mips(line):
    mips = []
    bit_string = ""
    for i in range(len(line)):
        bit_string += line[i]
        if len(bit_string) == 32:
            op_code = bit_string[0:6]
            if op_code == "000000":
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
                    mips.append(f"UNKNOWN_FUNC {func_code}")
            elif op_code in ["100011", "101011"]:  # lw, sw
                rs, rt, offset = bit_string[6:11], bit_string[11:16], bit_string[16:32]
                instr = op_codes.get(op_code, "UNKNOWN")
                mips.append(f"{instr} {registers[rt]}, {int(offset, 2)}({registers[rs]})")
            elif op_code in op_codes:
                instr = op_codes[op_code]
                if instr in {"dom", "maro", "ucl", "rmd", "egp", "fcb", "int", "lfc"}:
                    mips.append(instr)
                else:
                    rs, rt, offset = bit_string[6:11], bit_string[11:16], bit_string[16:32]
                    mips.append(f"{instr} {registers[rs]}, {registers[rt]}, {int(offset, 2)}")
            else:
                mips.append(f"UNKNOWN_OP {op_code}")
            bit_string = ""
    return mips


if __name__ == "__main__":
    handle_lines("DisassemblerInput.bin")
