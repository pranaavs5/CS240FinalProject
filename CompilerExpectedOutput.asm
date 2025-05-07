.data
fizz:       .asciiz "Fizz\n"
buzz:       .asciiz "Buzz\n"
fizzbuzz:   .asciiz "FizzBuzz\n"
newline:    .asciiz "\n"

.text
.globl main

main:
    li $t0, 1              # counter i = 1

loop:
    bgt $t0, 100, end      # if i > 100, end loop

    # check divisible by 3
    li $t1, 3
    rem $t2, $t0, $t1      # t2 = i % 3
    li $t3, 0
    beq $t2, $t3, is_div3
    li $t4, 0              # not divisible by 3
    j check5
is_div3:
    li $t4, 1              # divisible by 3

check5:
    li $t1, 5
    rem $t2, $t0, $t1      # t2 = i % 5
    li $t3, 0
    beq $t2, $t3, is_div5
    li $t5, 0              # not divisible by 5
    j print
is_div5:
    li $t5, 1              # divisible by 5

print:
    # Check for FizzBuzz
    li $t6, 1
    beq $t4, $t6, check_fizzbuzz
    j check_fizz
check_fizzbuzz:
    beq $t5, $t6, print_fizzbuzz
    j check_fizz

print_fizzbuzz:
    li $v0, 4              # syscall to print string
    la $a0, fizzbuzz
    syscall
    j increment

check_fizz:
    beq $t4, $t6, print_fizz
    j check_buzz

print_fizz:
    li $v0, 4
    la $a0, fizz
    syscall
    j increment

check_buzz:
    beq $t5, $t6, print_buzz
    j print_num

print_buzz:
    li $v0, 4
    la $a0, buzz
    syscall
    j increment

print_num:
    li $v0, 1
    move $a0, $t0
    syscall
    li $v0, 4
    la $a0, newline
    syscall

increment:
    addi $t0, $t0, 1
    j loop

end:
    li $v0, 10             # exit
    syscall
