"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0]*8  # R0-R7 - variables in hardware w/ fixed names and number of registers.
        self.ram = [0]*256  # memory 
        self.pc = 0  # Program Couter - address of the current excecuted instruction
        self.address = 0
        self.runs = True
        self.sp = len(self.reg)  # STACK POINTER
        self.bht = {
            0b00000001: self.op_HLT,
            0b10000010: self.op_LDI,
            0b01000111: self.op_PRN,
            0b10100010: self.op_MUL,
            0b01000101: self.op_PUSH,
            0b01000110: self.op_POP,
        }

    def load(self):
        """Load a program into memory."""

        # address = 0

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010,  # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111,  # PRN R0
        #     0b00000000,
        #     0b00000001,  # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1

        self.address = 0

        if len(sys.argv) < 2:
            print('Error, lacking arguments')
            sys.exit(0)

        try:
            with open(sys.argv[1]) as f:
                for line in f:
                    t = line.split()
                    n = line.strip()

                    if len(t) == 0:
                        continue
                    if t[0][0] == '#':
                        continue
                    try:
                        self.ram[self.address] = int(t[0], 2)
                    except ValueError:
                        print(f"Invalid number {n} ")
                        sys.exit(1)

                    self.address += 1
        except FileNotFoundError:
            print(f"Not a valid number - {t[0]}")
            sys.exit(2)

        if self.address == 0:
            print('no input into program')

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        # ______________DAY 1 CODE
        # if op == "ADD":
        #     self.reg[reg_a] += self.reg[reg_b]
        # #elif op == "SUB": etc
        # _______________DAY 2 CODE
        a = self.reg[reg_a]
        b = self.reg[reg_b]
        if op == "ADD":
            a += b
        elif op == 'SUB':
            a -= b
        elif op == 'MUL':
            a *= b
        elif op == 'DIV':
            a /= b
        else:
            raise Exception("Unsupported ALU operation")

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, address, value):
        self.ram[address] = value

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
        self.load()
        while self.runs:
            command = self.ram[self.pc]
            if command in self.bht:
                func = self.bht[command]
                func()
                # self.trace()
            else:
                print(command, 'Not a valid command')
                break

    def op_HLT(self):
        # halt
        self.runs = False

    def op_LDI(self):
        # set reg val to int

        op_a = self.ram_read(self.pc + 1)
        op_b = self.ram_read(self.pc + 2)
        self.reg[op_a] = op_b
        self.pc += 3

    def op_PRN(self):
        op_a = self.ram_read(self.pc + 1)
        print(self.reg[op_a])
        self.pc += 2

    def op_MUL(self):
        op_a = self.ram_read(self.pc + 1)
        op_b = self.ram_read(self.pc + 2)
        self.reg[op_a] *= self.reg[op_b]
        self.pc += 3

    def op_PUSH(self):
        self.sp -= 1
        self.reg[self.sp] = self.reg[self.ram[self.pc + 1]]  # PUSH VALUE TO RAM @ PC INTO STACK AND SAVE VALUE IN STACK
        self.pc += 2

    def op_POP(self):
        self.reg[self.ram[self.pc + 1]] = self.reg[self.sp]  # POP FROM STACK AND ADD TO REGISTER
        self.sp += 1
        self.pc += 2

            # #___________________DAY 3 CODE _____________________________ 
            # elif command == 0b01000101:
            #     self.sp -= 1
            #     self.reg[self.sp] = self.reg[self.ram[self.pc + 1]]  # PUSH VALUE TO RAM @ PC INTO STACK AND SAVE VALUE IN STACK
            #     self.pc += 2
            # elif command == 0b01000110:
            #     self.reg[self.ram[self.pc + 1]] = self.reg[self.sp]  # POP FROM STACK AND ADD TO REGISTER
            #     self.sp += 1
            #     self.pc += 2


            # #_________________________________________________________
            # else:
            #     self.runs = False
            #     print(f"Invalid input {command}")
                

