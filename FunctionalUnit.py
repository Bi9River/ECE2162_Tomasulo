from ReservationStation import ReservationStation
from LoadStoreQueue import LoadStoreQueue

class FunctionalUnit(object):
    def __init__(self, supportedIns, cyclenums, rs_size_dict):
        self.supportedInstructions = supportedIns
        self.cycles = cyclenums
        self.reservationStation = []
        self.loadstorequeue = []
        op_type = supportedIns[0]
        if ('Mult' in op_type) or ('Add' in op_type):
            if '.d' in op_type:
                data_type = 'fp'
            else:
                data_type = 'int'
            if 'Add' in op_type:
                op_type = 'add'
            elif 'Mul' in op_type:
                op_type = 'mul'
            rs_key = data_type + '_' + op_type
            for i in range(rs_size_dict[rs_key]):
                self.reservationStation.append(ReservationStation())  # TODO: using RS instead of LSQ?
        elif ('Ld' in op_type) or ('Store' in op_type):
            for i in range(10):     # set the size of LSQ
                self.loadstorequeue.append(LoadStoreQueue())    # TODO: check Load and Store
            pass

    def clear (self):
        self.reservationStation = ReservationStation()


class FunctionalUnits(object):
    def __init__(self):
        self.fuList = []

    def add(self, fu):
        self.fuList.append(fu)

    def findAvailable(self, opname):    # TODO: return the first available RS
        for funtionalunit in self.fuList:
            if opname in funtionalunit.supportedInstructions:
                for rs in funtionalunit.reservationStation:
                    if not rs.busy:
                        # if opname in funtionalunit.supportedInstructions:
                        return rs, funtionalunit.cycles
        return False

    def isAvailable(self, opname):
        for fu in self.fuList:
            for rs in fu.reservationStation:
                if opname in fu.supportedInstructions:
                    if not rs.busy:
                        return True
        return False

    def findAvailableLSQ(self):
        for fu in self.fuList:
           if fu.supportedInstructions == ['Ld', 'Sd']:
                for lsq in fu.loadstorequeue:
                    if not lsq.busy:
                        return lsq    # TODO: does it need cycles?
        return False

    def flush(self,list):
        for fu in self.fuList:
            for robId in list:
                rs = fu.reservationStation
                if rs.Qj == robId or rs.Qk == robId or rs.destination == robId:
                    fu.clear()

    def toString(self):
        st = 'Reservation Stations\n'
        i = 0
        for fu in self.fuList:
            for rs in fu.reservationStation:
                st += 'RS' + str(i) + ': ' + rs.toString() + '\n'
                i += 1
        return st