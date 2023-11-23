from collections import deque


class Instruction(object):
    def __init__(self, adrs, op, dest, s1, s2=None):
        self.adress = adrs    # is the pc?
        self.opname = op
        self.destination = dest
        self.source1 = s1   # operand1 and operand2/offset and operand(for Ld and Sd
        self.source2 = s2

    def toString(self):
        st = ''
        if self.opname == 'Ld':
            st = self.opname + '  ' + str(self.destination) + ', ' + str(self.source1) + '(' + str(self.source2) + ')'
        elif self.opname == 'Bne':
            st = self.opname + ' ' + str(self.source1) + ', ' + str(self.source2) + ', ' + str(self.destination)
        else:
            st = self.opname + ' ' + self.destination + ', ' + str(self.source1) + ', ' + str(self.source2)
        return st


class InstructionBuffer(object):
    def __init__(self, window_size):
        self.instructions = deque()
        self.window_size = window_size

    def add(self, instruction):
        self.instructions.append(instruction)

    def isEmpty(self):
        if len(self.instructions) == 0:
            return True
        else:
            return False

    def isFull(self):
        if len(self.instructions) == self.window_size:
            return True
        else:
            return False

    def head(self):
        return self.instructions[0]

    def pop(self):
        return self.instructions.popleft()

    def clear(self):
        self.instructions = deque()

    def toString(self):
        st = "Instruction Window\n"
        for i in self.instructions:
            st += i.toString() + '\n'
        return st
