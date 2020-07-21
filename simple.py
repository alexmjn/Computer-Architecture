
PRINT_NAME    = 0b01
HALT          = 0b10
PRINT_NUM     = 0b11
SAVE = 0b100
PRINT_REG = 0b101

# save the number 99 into R2
# R0-R7 are the names of the registers
memory = [
    PRINT_NAME,
    PRINT_NAME,
    PRINT_NAME,
    PRINT_NUM,
# how to give a number to a function
    42,
    SAVE,
    2,
    99,
    PRINT_REG,
    HALT,
]

registers = [0] * 8

# write a program to pull each command out of memory and execute it
# program is stored in ram
program_counter = 0
running = True
while running:
    command = memory[program_counter]
    if command == PRINT_NAME:
        print("name")

    if command == HALT:
        break

    if command == PRINT_NUM:
        program_counter += 1
        print(memory[program_counter])

    if command == SAVE:
        index = memory[program_counter + 1]
        number = memory[program_counter + 2]
        registers[index] = number
        program_counter += 2

    program_counter = program_counter + 1
