memoryAddress = 5000
tRegister = 0
vars = dict()
label_count = 0
current_label = None
while_blocks = []
if_blocks = []

def getInstructionLine(varName):
    global tRegister, memoryAddress
    tRegisterName = f"$t{tRegister}"
    setVariableRegister(varName, tRegisterName)
    returnText = f"bump {tRegisterName}, $zero, {memoryAddress}"
    tRegister += 1
    memoryAddress += 4
    return returnText

def setVariableRegister(varName, tRegister):
    global vars
    vars[varName] = tRegister

def getVariableRegister(varName):
    global vars
    if varName in vars:
        return vars[varName]
    else:
        return "ERROR"

def getAssignmentLinesImmediateValue(val, varName):
    global tRegister
    outputText = f"""bump $t{tRegister}, $zero, {val}
save $t{tRegister}, 0({getVariableRegister(varName)})"""
    tRegister += 1
    return outputText

def getAssignmentLinesVariable(varSource, varDest):
    global tRegister
    outputText = ""
    registerSource = getVariableRegister(varSource)
    outputText = f"grab $t{tRegister}, 0({registerSource})" + "\n"
    tRegister += 1
    registerDest = getVariableRegister(varDest)
    outputText += f"save $t{tRegister-1}, 0({registerDest})"
    return outputText

def getOperationLines(var1, op, var2, dest):
    global tRegister
    outputText = ""
    
    if var1 in vars:
        outputText += f"grab $t{tRegister}, 0({getVariableRegister(var1)})\n"
    elif var1.isdigit():
        outputText += f"bump $t{tRegister}, $zero, {var1}\n"
    
    t1 = tRegister
    tRegister += 1
    
    if var2 in vars:
        outputText += f"grab $t{tRegister}, 0({getVariableRegister(var2)})\n"
    elif var2.isdigit():
        outputText += f"bump $t{tRegister}, $zero, {var2}\n"
    
    t2 = tRegister
    tRegister += 1
    
    if op == "+":
        outputText += f"sum $t{tRegister}, $t{t1}, $t{t2}\n"
    elif op == "-":
        outputText += f"dif $t{tRegister}, $t{t1}, $t{t2}\n"
    elif op == "*":
        outputText += f"bump $t{tRegister}, $zero, 0\n"
        temp_label = f"mult_{label_count}"
        end_label = f"end_mult_{label_count}"
        next_label = label_count
        label_count += 1
        
        outputText += f"bump $t{tRegister+1}, $zero, 0\n"
        
        outputText += f"{temp_label}:\n"
        
        outputText += f"when $t{tRegister+1}, $t{t2}, {end_label}\n"
        
        outputText += f"sum $t{tRegister}, $t{tRegister}, $t{t1}\n"
        
        outputText += f"bump $t{tRegister+1}, $t{tRegister+1}, 1\n"
        
        outputText += f"skip $zero, $zero, {temp_label}\n"
        
        outputText += f"{end_label}:\n"
        
        tRegister += 2
    elif op == "/":
        outputText += f"bump $t{tRegister}, $t{t1}, 0\n"
        outputText += f"bump $t{tRegister+1}, $zero, 0\n"
        
        temp_label = f"div_{label_count}"
        end_label = f"end_div_{label_count}"
        label_count += 1
        
        outputText += f"{temp_label}:\n"
        
        outputText += f"less $t{tRegister+2}, $t{tRegister}, $t{t2}\n"
        outputText += f"when $t{tRegister+2}, $t{t2}, {end_label}\n"
        
        outputText += f"dif $t{tRegister}, $t{tRegister}, $t{t2}\n"
        
        outputText += f"bump $t{tRegister+1}, $t{tRegister+1}, 1\n"
        
        outputText += f"skip $zero, $zero, {temp_label}\n"
        
        outputText += f"{end_label}:\n"
        
        outputText += f"bump $t{tRegister}, $t{tRegister+1}, 0\n"
        
        tRegister += 3
    elif op == "%":
        outputText += f"bump $t{tRegister}, $t{t1}, 0\n"
        
        temp_label = f"mod_{label_count}"
        end_label = f"end_mod_{label_count}"
        label_count += 1
        
        outputText += f"{temp_label}:\n"
        
        outputText += f"less $t{tRegister+1}, $t{tRegister}, $t{t2}\n"
        outputText += f"when $t{tRegister+1}, $t{t2}, {end_label}\n"
        
        outputText += f"dif $t{tRegister}, $t{tRegister}, $t{t2}\n"
        
        outputText += f"skip $zero, $zero, {temp_label}\n"
        
        outputText += f"{end_label}:\n"
        
        tRegister += 2
    elif op == "&&":
        outputText += f"conj $t{tRegister}, $t{t1}, $t{t2}\n"
    elif op == "||":
        outputText += f"disj $t{tRegister}, $t{t1}, $t{t2}\n"
    elif op == "<":
        outputText += f"less $t{tRegister}, $t{t1}, $t{t2}\n"
    elif op == ">":
        outputText += f"less $t{tRegister}, $t{t2}, $t{t1}\n"
    elif op == "==":
        outputText += f"less $t{tRegister}, $t{t1}, $t{t2}\n"
        outputText += f"less $t{tRegister+1}, $t{t2}, $t{t1}\n"
        
        outputText += f"dif $t{tRegister}, $zero, $t{tRegister}\n"
        outputText += f"bump $t{tRegister}, $t{tRegister}, 1\n"
        
        outputText += f"dif $t{tRegister+1}, $zero, $t{tRegister+1}\n"
        outputText += f"bump $t{tRegister+1}, $t{tRegister+1}, 1\n"
        
        outputText += f"conj $t{tRegister}, $t{tRegister}, $t{tRegister+1}\n"
        
        tRegister += 1
    elif op == "!=":
        outputText += f"less $t{tRegister}, $t{t1}, $t{t2}\n"
        outputText += f"less $t{tRegister+1}, $t{t2}, $t{t1}\n"
        
        outputText += f"disj $t{tRegister}, $t{tRegister}, $t{tRegister+1}\n"
        
        tRegister += 1
    elif op == "<=":
        outputText += f"less $t{tRegister}, $t{t1}, $t{t2}\n"
        
        outputText += f"less $t{tRegister+1}, $t{t1}, $t{t2}\n"
        outputText += f"less $t{tRegister+2}, $t{t2}, $t{t1}\n"
        
        outputText += f"dif $t{tRegister+1}, $zero, $t{tRegister+1}\n"
        outputText += f"bump $t{tRegister+1}, $t{tRegister+1}, 1\n"
        
        outputText += f"dif $t{tRegister+2}, $zero, $t{tRegister+2}\n"
        outputText += f"bump $t{tRegister+2}, $t{tRegister+2}, 1\n"
        
        outputText += f"conj $t{tRegister+1}, $t{tRegister+1}, $t{tRegister+2}\n"
        
        outputText += f"disj $t{tRegister}, $t{tRegister}, $t{tRegister+1}\n"
        
        tRegister += 2
    elif op == ">=":
        outputText += f"less $t{tRegister}, $t{t2}, $t{t1}\n"
        
        outputText += f"less $t{tRegister+1}, $t{t1}, $t{t2}\n"
        outputText += f"less $t{tRegister+2}, $t{t2}, $t{t1}\n"
        
        outputText += f"dif $t{tRegister+1}, $zero, $t{tRegister+1}\n"
        outputText += f"bump $t{tRegister+1}, $t{tRegister+1}, 1\n"
        
        outputText += f"dif $t{tRegister+2}, $zero, $t{tRegister+2}\n"
        outputText += f"bump $t{tRegister+2}, $t{tRegister+2}, 1\n"
        
        outputText += f"conj $t{tRegister+1}, $t{tRegister+1}, $t{tRegister+2}\n"
        
        outputText += f"disj $t{tRegister}, $t{tRegister}, $t{tRegister+1}\n"
        
        tRegister += 2
    
    tRegister += 1
    
    if dest in vars:
        outputText += f"save $t{tRegister-1}, 0({getVariableRegister(dest)})"
    
    return outputText

def parse_c_program(input_file):
    global tRegister, label_count, current_label, while_blocks, if_blocks
    
    with open(input_file, "r") as f:
        lines = f.readlines()
    
    outputText = ""
    in_if_block = False
    in_else_block = False
    in_while_block = False
    line_num = 0
    
    while line_num < len(lines):
        line = lines[line_num].strip()
        line_num += 1
        
        if not line:
            continue
            
        if line.startswith("//"):
            continue
            
        if line.startswith("int "):
            parts = line.split("int ")
            var = parts[1].strip()
            if ";" in var:
                var = var.split(";")[0].strip()
            outputText += getInstructionLine(var) + "\n"
            
        elif line.startswith("while "):
            expr = line.replace("while", "").strip()
            expr = expr[1:-1]
            
            start_label = f"while_{label_count}"
            end_label = f"endwhile_{label_count}"
            label_count += 1
            
            while_blocks.append((start_label, end_label))
            
            outputText += f"{start_label}:\n"
            
            parts = expr.split()
            if len(parts) == 3:
                var1, op, var2 = parts
                
                cond_code = getOperationLines(var1, op, var2, None)
                outputText += cond_code + "\n"
                
                if op == "==":
                    outputText += f"skip $t{tRegister-1}, $zero, {end_label}\n"
                elif op == "!=":
                    outputText += f"when $t{tRegister-1}, $zero, {end_label}\n"
                elif op == "<":
                    outputText += f"when $t{tRegister-1}, $zero, {end_label}\n"
                elif op == ">":
                    outputText += f"when $t{tRegister-1}, $zero, {end_label}\n"
                elif op == "<=":
                    outputText += f"when $t{tRegister-1}, $zero, {end_label}\n"
                elif op == ">=":
                    outputText += f"when $t{tRegister-1}, $zero, {end_label}\n"
            
            in_while_block = True
            
        elif line.startswith("if "):
            expr = line.replace("if", "").strip()
            expr = expr[1:-1]
            if expr.endswith("{"):
                expr = expr[:-1].strip()
            
            true_label = f"if_{label_count}"
            false_label = f"else_{label_count}"
            end_label = f"endif_{label_count}"
            label_count += 1
            
            if_blocks.append((true_label, false_label, end_label))
            
            parts = expr.split()
            if len(parts) == 3:
                var1, op, var2 = parts
                
                cond_code = getOperationLines(var1, op, var2, None)
                outputText += cond_code + "\n"
                
                if op == "==":
                    outputText += f"skip $t{tRegister-1}, $zero, {false_label}\n"
                elif op == "!=":
                    outputText += f"when $t{tRegister-1}, $zero, {false_label}\n"
                elif op == "<":
                    outputText += f"when $t{tRegister-1}, $zero, {false_label}\n"
                elif op == ">":
                    outputText += f"when $t{tRegister-1}, $zero, {false_label}\n"
                elif op == "<=":
                    outputText += f"when $t{tRegister-1}, $zero, {false_label}\n"
                elif op == ">=":
                    outputText += f"when $t{tRegister-1}, $zero, {false_label}\n"
            elif "&&" in expr or "||" in expr:
                if "&&" in expr:
                    subconds = expr.split("&&")
                    
                    subcond1 = subconds[0].strip()
                    parts1 = subcond1.split()
                    if len(parts1) == 3:
                        var1, op1, var2 = parts1
                        cond_code1 = getOperationLines(var1, op1, var2, None)
                        outputText += cond_code1 + "\n"
                        
                        if op1 == "==":
                            outputText += f"skip $t{tRegister-1}, $zero, {false_label}\n"
                        elif op1 == "!=":
                            outputText += f"when $t{tRegister-1}, $zero, {false_label}\n"
                        elif op1 == "<":
                            outputText += f"when $t{tRegister-1}, $zero, {false_label}\n"
                        elif op1 == ">":
                            outputText += f"when $t{tRegister-1}, $zero, {false_label}\n"
                        elif op1 == "<=":
                            outputText += f"when $t{tRegister-1}, $zero, {false_label}\n"
                        elif op1 == ">=":
                            outputText += f"when $t{tRegister-1}, $zero, {false_label}\n"
                    
                    subcond2 = subconds[1].strip()
                    parts2 = subcond2.split()
                    if len(parts2) == 3:
                        var1, op2, var2 = parts2
                        cond_code2 = getOperationLines(var1, op2, var2, None)
                        outputText += cond_code2 + "\n"
                        
                        if op2 == "==":
                            outputText += f"skip $t{tRegister-1}, $zero, {false_label}\n"
                        elif op2 == "!=":
                            outputText += f"when $t{tRegister-1}, $zero, {false_label}\n"
                        elif op2 == "<":
                            outputText += f"when $t{tRegister-1}, $zero, {false_label}\n"
                        elif op2 == ">":
                            outputText += f"when $t{tRegister-1}, $zero, {false_label}\n"
                        elif op2 == "<=":
                            outputText += f"when $t{tRegister-1}, $zero, {false_label}\n"
                        elif op2 == ">=":
                            outputText += f"when $t{tRegister-1}, $zero, {false_label}\n"
                
                elif "||" in expr:
                    subconds = expr.split("||")
                    
                    subcond1 = subconds[0].strip()
                    parts1 = subcond1.split()
                    if len(parts1) == 3:
                        var1, op1, var2 = parts1
                        cond_code1 = getOperationLines(var1, op1, var2, None)
                        outputText += cond_code1 + "\n"
                        
                        if op1 == "==":
                            outputText += f"when $t{tRegister-1}, $zero, {true_label}\n"
                        elif op1 == "!=":
                            outputText += f"skip $t{tRegister-1}, $zero, {true_label}\n"
                        elif op1 == "<":
                            outputText += f"skip $t{tRegister-1}, $zero, {true_label}\n"
                        elif op1 == ">":
                            outputText += f"skip $t{tRegister-1}, $zero, {true_label}\n"
                        elif op1 == "<=":
                            outputText += f"skip $t{tRegister-1}, $zero, {true_label}\n"
                        elif op1 == ">=":
                            outputText += f"skip $t{tRegister-1}, $zero, {true_label}\n"
                    
                    subcond2 = subconds[1].strip()
                    parts2 = subcond2.split()
                    if len(parts2) == 3:
                        var1, op2, var2 = parts2
                        cond_code2 = getOperationLines(var1, op2, var2, None)
                        outputText += cond_code2 + "\n"
                        
                        if op2 == "==":
                            outputText += f"skip $t{tRegister-1}, $zero, {false_label}\n"
                        elif op2 == "!=":
                            outputText += f"when $t{tRegister-1}, $zero, {false_label}\n"
                        elif op2 == "<":
                            outputText += f"when $t{tRegister-1}, $zero, {false_label}\n"
                        elif op2 == ">":
                            outputText += f"when $t{tRegister-1}, $zero, {false_label}\n"
                        elif op2 == "<=":
                            outputText += f"when $t{tRegister-1}, $zero, {false_label}\n"
                        elif op2 == ">=":
                            outputText += f"when $t{tRegister-1}, $zero, {false_label}\n"
                    
                    outputText += f"{true_label}:\n"
            
            in_if_block = True
            
        elif line.startswith("else"):
            if if_blocks:
                _, false_label, end_label = if_blocks[-1]
                
                outputText += f"skip $zero, $zero, {end_label}\n"
                
                outputText += f"{false_label}:\n"
                
                in_if_block = False
                in_else_block = True
            
        elif line.startswith("}"):
            if in_if_block or in_else_block:
                if if_blocks:
                    _, _, end_label = if_blocks.pop()
                    outputText += f"{end_label}:\n"
                    in_if_block = False
                    in_else_block = False
            elif in_while_block:
                if while_blocks:
                    start_label, end_label = while_blocks.pop()
                    outputText += f"skip $zero, $zero, {start_label}\n"
                    outputText += f"{end_label}:\n"
                    in_while_block = False
            
        elif line.startswith("return"):
            continue
            
        elif "print" in line:
            if "Fizzbuzz" in line or "FizzBuzz" in line:
                outputText += "maro\n"
            elif "Fizz" in line:
                outputText += "rmd\n"
            elif "Buzz" in line:
                outputText += "ucl\n"
            else:
                outputText += "fcb\n"
                
        elif "=" in line and not "==" in line and not "<=" in line and not ">=" in line and not "!=" in line:
            line = line.rstrip(";")
            
            if "+" in line or "-" in line or "*" in line or "/" in line or "%" in line:
                parts = line.split("=")
                dest = parts[0].strip()
                expr = parts[1].strip()
                
                if "+" in expr:
                    operands = expr.split("+")
                    var1 = operands[0].strip()
                    var2 = operands[1].strip()
                    outputText += getOperationLines(var1, "+", var2, dest) + "\n"
                elif "-" in expr:
                    operands = expr.split("-")
                    var1 = operands[0].strip()
                    var2 = operands[1].strip()
                    outputText += getOperationLines(var1, "-", var2, dest) + "\n"
                elif "*" in expr:
                    operands = expr.split("*")
                    var1 = operands[0].strip()
                    var2 = operands[1].strip()
                    outputText += getOperationLines(var1, "*", var2, dest) + "\n"
                elif "/" in expr:
                    operands = expr.split("/")
                    var1 = operands[0].strip()
                    var2 = operands[1].strip()
                    outputText += getOperationLines(var1, "/", var2, dest) + "\n"
                elif "%" in expr:
                    operands = expr.split("%")
                    var1 = operands[0].strip()
                    var2 = operands[1].strip()
                    outputText += getOperationLines(var1, "%", var2, dest) + "\n"
            else:
                parts = line.split("=")
                varName = parts[0].strip()
                val = parts[1].strip()
                
                if val.isdigit():
                    outputText += getAssignmentLinesImmediateValue(val, varName) + "\n"
                else:
                    outputText += getAssignmentLinesVariable(val, varName) + "\n"
    
    return outputText

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        output_file = input_file.replace(".c", ".asm")
        if len(sys.argv) > 2:
            output_file = sys.argv[2]
            
        code = parse_c_program(input_file)
        
        with open(output_file, "w") as f:
            f.write(code)
        
        print(f"Compiled {input_file} to {output_file}")
    else:
        code = parse_c_program("fizzbuzz.c")
        with open("fizzbuzz.asm", "w") as f:
            f.write(code)
        print("Compiled fizzbuzz.c to fizzbuzz.asm")
        
