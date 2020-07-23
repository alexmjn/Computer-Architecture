"""CPU functionality."""

import sys

ADD = 0b10100000
SUB = 0b10100001
MUL = 0b10100010
DIV = 0b10100011
MOD = 0b10100100

INC = 0b01100101
DEC = 0b01100110

CALL = 0b01010000
RET = 0b00010001

NOP = 0b00000000
HLT = 0b00000001 # halt, exit emulator
LDI = 0b10000010 # load "immediate", store a value, set a register to a value

PRN = 0b01000111
PUSH = 0b01000101
POP = 0b01000110

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.reg[7] = 0xF4
        self.pc = 0 #program counter
        self.sp = self.reg[7]
        self.mar = None # memory access register
        self.mdr = None # memory register
        self.branch_table = {
            HLT: self.hlt,
            LDI: self.ldi,
            PRN: self.prn,
            POP: self.pop,
            PUSH: self.push,
            ADD: self.add,
            SUB: self.sub,
            MUL: self.mul,
            DIV: self.div,
        }

    def hlt(self):
        sys.exit()

    def ldi(self, op_a, op_b):
        self.reg[op_a] = op_b

    def prn(self, op_a):
        print(self.reg[op_a])

    def pop(self, reg_num):
        self.reg[reg_num] = self.ram_read(self.reg[7])
        self.reg[7] += 1

    def push(self, reg_num):
        self.reg[7] -= 1
        self.ram_write(self.reg[reg_num], self.reg[7])

    def add(self, op_a, op_b):
        self.reg[op_a] += self.reg[op_b]

    def sub(self, op_a, op_b):
        self.reg[op_a] -= self.reg[op_b]

    def mul(self, op_a, op_b):
        self.reg[op_a] *= self.reg[op_b]

    def div(self, op_a, op_b):
        self.reg[op_a] /= self.reg[op_b]


    def ram_write(self, address, value):
        self.ram[address] = value

    def ram_read(self, address):
        try:
            return self.ram[address]
        except KeyError:
            print("Invalid Register")
            return None

    def load(self, filename):
        """Load a program into memory."""
        basePath = './examples/'
        file = 'print8.ls8'
        if len(sys.argv) > 1:
            file = sys.argv[1]
        address = 0

        with open(basePath + file, 'r') as f:
            for line in f:
                line = line.split("#")

                try:
                    instruction = int(line[0], 2)
                except ValueError:
                    continue

                self.ram[address] = instruction
                address += 1




    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU.
        reads memory address and stores result in IR
        """
        self.IR = self.ram_read(self.pc)
        operand_a = self.ram_read(self.pc + 1)
        operand_b = self.ram_read(self.pc + 2)

        while self.IR != HLT:
            num_arguments = ((self.IR & 0b11000000) >> 6)


            if num_arguments == 0:
                self.branch_table[self.IR]

            elif num_arguments == 1:
                self.branch_table[self.IR](operand_a)

            else:
                self.branch_table[self.IR](operand_a, operand_b)


            self.pc += (num_arguments + 1)
            self.IR = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
