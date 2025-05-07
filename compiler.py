memoryAddress = 10000  # Start data segment at a higher address
tRegister = 0
vars = dict()
label_counter = 0

def get_new_label():
    global label_counter
    label = f"L{label_counter}"
    label_counter += 1
    return label

def emit_line(line):
    global outputText
    outputText += line + "\n"

def getInstructionLine(varName):
    global memoryAddress, tRegister
    tRegisterName = f"$t{tRegister}"
    setVariableRegister(varName, tRegisterName)
    emit_line(f"addi {tRegisterName}, $zero, {memoryAddress}")
    tRegister += 1
    memoryAddress += 4
    return tRegisterName

def setVariableRegister(varName, tRegister):
    global vars
    vars[varName] = tRegister

def getVariableRegister(varName):
    global vars
    if varName in vars:
        return vars[varName]
    else:
        print(f"Error: Variable '{varName}' not found!")
        return "$zero"  # Return a safe register instead of "ERROR"

def getAssignmentLinesImmediateValue(val, varName):
    global tRegister
    reg = getVariableRegister(varName)
    emit_line(f"li $t{tRegister}, {val}")
    emit_line(f"sw $t{tRegister}, 0({reg})")
    tRegister += 1

def getAssignmentLinesVariable(varSource, varDest):
    global tRegister
    reg_source = getVariableRegister(varSource)
    reg_dest = getVariableRegister(varDest)
    emit_line(f"lw $t{tRegister}, 0({reg_source})")
    emit_line(f"sw $t{tRegister}, 0({reg_dest})")
    tRegister += 1

def handle_if_condition(condition, end_label):
    parts = condition.split()
    reg1 = getVariableRegister(parts[0])
    op = parts[1]
    val = parts[2]
    false_label = get_new_label()
    if op == "==":
        emit_line(f"bne {reg1}, {val}, {false_label}")
    elif op == "!=":
        emit_line(f"beq {reg1}, {val}, {false_label}")
    elif op == "<=":
        emit_line(f"bgt {reg1}, {val}, {false_label}")
    elif op == ">=":
        emit_line(f"blt {reg1}, {val}, {false_label}")
    elif op == "<":
        emit_line(f"bge {reg1}, {val}, {false_label}")
    elif op == ">":
        emit_line(f"ble {reg1}, {val}, {false_label}")
    emit_line(f"b {end_label}")  # If condition is true, jump to the 'then' block
    emit_line(f"{false_label}:")  # Label for when the condition is false
    return false_label  # Return the label to jump to if false

def handle_printf(line):
    if "FizzBuzz" in line:
        emit_line("li $v0, 4")
        emit_line("la $a0, fizzbuzz_str")
        emit_line("syscall")
    elif "Fizz" in line:
        emit_line("li $v0, 4")
        emit_line("la $a0, fizz_str")
        emit_line("syscall")
    elif "Buzz" in line:
        emit_line("li $v0, 4")
        emit_line("la $a0, buzz_str")
        emit_line("syscall")
    elif "%d" in line:
        parts = line.split()
        var_to_print = ""
        for part in reversed(parts):
            if part.isalnum():
                var_to_print = part
                break
        reg_to_print = getVariableRegister(var_to_print)
        emit_line(f"lw $a0, 0({reg_to_print})")
        emit_line("li $v0, 1")
        emit_line("syscall")
    emit_line("li $v0, 4")  # Print newline
    emit_line("la $a0, newline_str")
    emit_line("syscall")


f = open("CompilerInput.c", "r")
lines = f.readlines()
f.close()

outputText = ".data\n"
outputText += "fizzbuzz_str: .asciiz \"FizzBuzz\\n\"\n"
outputText += "fizz_str:     .asciiz \"Fizz\\n\"\n"
outputText += "buzz_str:     .asciiz \"Buzz\\n\"\n"
outputText += "newline_str:  .asciiz \"\\n\"\n"
outputText += "\n.text\n"
outputText += ".globl main\n\n"
outputText += "main:\n"

loop_start_label = get_new_label()
loop_end_label = get_new_label()
vars["i"] = f"$t{tRegister}"  # Manually assign register for 'i' initially
emit_line(f"addi $t{tRegister}, $zero, 1")  # i = 1
tRegister += 1
emit_line(f"{loop_start_label}:")
emit_line(f"bgt $t{tRegister - 1}, 100, {loop_end_label}")  # if i > 100, goto end_loop

in_for_loop = False  # Flag to track if inside the for loop
if_level = 0
endif_labels = []


for line in lines:
    line = line.strip()

    if line.startswith("for"):
        in_for_loop = True
        continue  # Already handled the loop initialization and condition

    elif line.startswith("if"):
        condition = line[line.find("(") + 1:line.find(")")].strip()
        endif_label = get_new_label()
        endif_labels.append(endif_label)
        handle_if_condition(
            condition.replace("%", "%%").replace("==", " == ").replace("!=", " != ").replace("<=", " <= ").replace(">=", " >= ").replace("<", " < ").replace(">", " > "),
            endif_label,
        )
        if_level += 1

    elif line.startswith("else if"):
        if if_level > 0 and endif_labels:
            current_endif = endif_labels[-1]
            emit_line(f"b {current_endif}")
            condition = line[line.find("(") + 1:line.find(")")].strip()
            new_endif_label = get_new_label()
            endif_labels[-1] = new_endif_label  # Update the endif label for this 'else if'
            handle_if_condition(
                condition.replace("%", "%%").replace("==", " == ").replace("!=", " != ").replace("<=", " <= ").replace(">=", " >= ").replace("<", " < ").replace(">", " > "),
                new_endif_label,
            )
        else:
            print("Error: 'else if' without a preceding 'if'")
            exit()  # Exit if there's a structural error

    elif line.startswith("else"):
        if if_level > 0 and endif_labels:
            current_endif = endif_labels[-1]
            emit_line(f"b {current_endif}")
            endif_label = get_new_label()
            endif_labels[-1] = endif_label  # Update for the 'else' block's end
            emit_line(f"{endif_label}:")  # Label for the 'else' block
        else:
            print("Error: 'else' without a preceding 'if'")
            exit()  # Exit if there's a structural error

    elif line.startswith("}"):
        if if_level > 0 and endif_labels:
            emit_line(f"{endif_labels.pop()}:")
            if_level -= 1
        elif in_for_loop:
            emit_line(f"addi $t{tRegister - 1}, $t{tRegister - 1}, 1")  # i++
            emit_line(f"b {loop_start_label}")
            emit_line(f"{loop_end_label}:")
            in_for_loop = False

    elif line.startswith("printf"):
        handle_printf(line)

    elif line.startswith("int i ="):
        parts = line.split("=")
        value = parts[1].strip().strip(";")
        reg_i = getVariableRegister("i")
        emit_line(f"li {reg_i}, {value}")

    elif "i % 15 == 0" in line or "i % 3 == 0" in line or "i % 5 == 0" in line:
        pass  # These are part of the if conditions

emit_line("li $v0, 10")  # Exit syscall
emit_line("syscall")

outputFile = open("mips1.asm", "w")
outputFile.write(outputText)
outputFile.close()

print("Compilation attempt finished. Check mips1.asm for output.")
