"""CPU functionality."""

import sys

ADD = 0b10100000
SUB = 0b10100001
MUL = 0b10100010
DIV = 0b10100011
PRN = 0b01000111

CALL = 0b01010000
RET = 0b00010001

NOP = 0b00000000
HTL = 0b00000001 # halt, exit emulator
LDI = 0b10000010 # load "immediate", store a value, set a register to a value

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0 #program counter
        self.sp = 0 #stack pointer
        self.mar = None # memory access register
        self.mdr = None # memory register

    def ram_write(self, mdr, mar):
        self.reg[mar] = mdr

    def ram_read(self, mar):
        try:
            return self.reg[mar]
        except KeyError:
            print("Invalid Register")
            return None

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

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
        """Run the CPU."""
        running = True
        while running:
            ir = ram_read(self.pc)
            operand_a = ram_read(self.pc + 1)
            operand_b = ram_read(self.pc + 2)

            if ir == HLT:
                sys.exit()

            elif ir == PRN:
