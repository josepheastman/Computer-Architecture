"""CPU functionality."""

import sys

LDI = 0b10000010
MUL = 0b10100010
PRN = 0b01000111
HLT = 0b00000001
PUSH = 0b01000101
POP = 0b01000110
CMP = 0b10100111
JMP = 0b01010100
JEQ = 0b01010101
JNE = 0b01010110


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.pc = 0
        self.reg = [0] * 8
        self.hlt = False
        self.sp = None
        self.fl = [0] * 8

        self.ops = {
            LDI: self.op_ldi,
            HLT: self.op_hlt,
            MUL: self.op_mul,
            PRN: self.op_prn,
            PUSH: self.push,
            POP: self.pop
        }

    def op_ldi(self, operand_a, operand_b):
        self.reg[operand_a] = operand_b

    def op_prn(self, operand_a, operand_b):
        print(self.reg[operand_a])

    def op_hlt(self, operand_a, operand_b):
        self.hlt = True

    def op_mul(self, operand_a, operand_b):
        self.alu('MUL', operand_a, operand_b)

    def push(self, operand_a, operand_b):
        self.reg[7] -= 1
        self.sp = self.reg[7]

        self.ram[self.sp] = self.reg[operand_a]

    def pop(self, operand_a, operand_b):
        self.sp = self.reg[7]

        operand_b = self.ram[self.sp]
        self.reg[operand_a] = operand_b

        self.reg[7] += 1

    def op_cmp(self, operand_a, operand_b):
        if operand_a < operand_b:
            self.fl = 1
        elif operand_a == operand_b:
            self.fl = 1
        elif operand_a > operand_b:
            self.fl = 1
        else:
            self.fl = 0

    def op_jmp(self, operand_a, operand_b):
        pass

    def op_jeq(self, operand_a, operand_b):
        pass

    def op_jne(self, operand_a, operand_b):
        pass

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, value, address):
        self.ram[address] = value

    def load(self, filename):
        """Load a program into memory."""

        address = 0

        with open(filename) as file:
            for line in file:
                comment_split = line.split('#')
                instruction = comment_split[0]

                if instruction == '':
                    continue

                first_bit = instruction[0]

                if first_bit == '0' or first_bit == '1':
                    self.ram[address] = int(instruction[:8], 2)
                    address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""

        while self.hlt == False:

            IR = self.ram[self.pc]
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            op_size = IR >> 6
            ins_set = ((IR >> 4) & 0b1) == 1

            if IR in self.ops:
                self.ops[IR](operand_a, operand_b)

            if not ins_set:
                self.pc += op_size + 1
