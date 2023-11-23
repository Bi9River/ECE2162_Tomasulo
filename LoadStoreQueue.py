
class LoadStoreQueue(object):     # TODO: add cyclesRemained = 4
    def __init__(self):
        self.opName = ''
        self.pc = None
        self.busy = False
        self.ready = False      # Ld and Sd have
        self.address = None
        self.value = None
        self.destination = None
        self.Vj = None
        self.Vk = None
        self.Qj = None
        self.Qk = None
        self.cyclesRemained = None       # will be set to 4 in issue state   # TODO: does it need robId? no

    def readFromMemory(self, memory):     # in execute stage, calculate the address
            self.address = self.Vj + self.Vk
            self.value = memory.getValue(self.address)

    # def setValue(self,memory):
    #     self.value = memory
