

class ReorderBuffer(object):
    def __init__(self, size=5):
        self.size = size
        self.head = 0
        self.tail = -1
        self.list = [ReorderBufferEntry(i) for i in range(self.size)]
        self.numelements = 0

    def isFull(self):
        if self.numelements == self.size:
            return True
        else:
            return False

    def createRobEntry(self, i):
        index = self.tail + 1
        index %= self.size
        self.list[index].opname = i.opname
        self.list[index].destination = i.destination
        self.list[index].busy = True
        self.tail += 1
        self.tail %= self.size
        self.numelements += 1
        return self.list[index].name

    def getHead(self):
        return self.list[self.head]

    def pop(self):
        self.list[self.head].clear()
        self.head += 1
        self.head %= self.size
        self.numelements -= 1

    def flush(self, destination):
        index = 0
        for entry in self.list:
            if entry.name == destination:
                index = self.list.index(entry)
                break

        listtoremove = []
        while (self.tail - index) % self.size != 0:
            index += 1
            index %= self.size
            listtoremove.append(self.list[index].name)
            self.list[index].clear()

        self.tail -= len(listtoremove)
        self.tail %= self.size
        self.numelements -= len(listtoremove)
        return listtoremove

    def toString(self):
        st = 'Reorder Buffer\n'
        i = 0
        for entry in self.list:
            st += entry.toString()
            if i == self.head:
                st += ' (H)'
            if i == self.tail:
                st += ' (T)'
            st += '\n'
            i += 1
        return st

    def findLastEntry(self, register):
        index = self.tail
        for i in range(self.numelements):  # ROB.numelements? public?
            if self.list[index].destination == register.name:  # Register or register?
                return self.list[index]
            index -= 1
            index %= self.size
        return None


class ReorderBufferEntry(object):
    def __init__(self, i):
        self.name = 'ROB' + str(i)
        self.opname = ''
        self.busy = False
        self.ready = False
        self.destination = ''
        self.value = None

    def clear(self):
        self.opname = ''
        self.busy = False
        self.ready = False
        self.destination = ''
        self.value = None

    def toString(self):
        st = self.name + ': '
        if self.ready:
            st += self.opname + ' '
            if self.opname == 'LD':
                st += ' '
            st += self.destination + ' ' + str(self.value)
        elif self.busy:
            st += self.opname + ' '
            if self.opname == 'LD':
                st += ' '
            st += self.destination + ' -'
        return st
