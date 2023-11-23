

class CommonDataBus(object):
    def __init__(self):
        self.value = None
        self.address = None
        self.busy = False

    def toString(self):
        st ='Common Data Bus\n'
        if self.busy:
            st += str(self.value) + ' ' + self.address
        return st