
class LoadStoreQueue(object):
    def __init__(self):
        self.opName = ''
        self.pc = None
        self.busy = False
        self.address = None
        self.value = None
        self.Vj = None
        self.Vk = None
        self.Qj = None
        self.Qk = None

    def execute(self):     # in execute stage, calculate the address
            address = self.Vj + self.Vk
            self.address = address

    def readMemory(self, memory):
            self.value = memory.getValue(self.address)
