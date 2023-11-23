from Register import Register


class RegisterFile(object):
    def __init__(self, num_of_registers):
        self.size = num_of_registers
        self.intRegPath = r'./int_register.txt'
        self.intRegisterList = []
        with open(self.intRegPath, 'r') as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip()
                line = line.split(':')
                self.intRegisterList.append(Register(line[0], int(line[1])))

        self.fpRegPath = r'./fp_register.txt'
        self.fpRegisterList = []
        with open(self.fpRegPath, 'r') as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip()
                line = line.split(':')
                self.fpRegisterList.append(Register(line[0], float(line[1])))

    def flush(self,list):
        for register in self.intRegisterList:
            for name in list:
                if register.robId == name:
                    register.clear()

    def toString(self):
        st = 'Registers\n'
        for reg in self.intRegisterList:
            st += reg.toString() + '\n'
        for reg in self.fpRegisterList:
            st += reg.toString() + '\n'
        return st


if __name__ == '__main__':
    registerFile = RegisterFile(16)
    print(registerFile.toString())
