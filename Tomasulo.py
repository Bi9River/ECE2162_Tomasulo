from LoadStoreQueue import LoadStoreQueue

def fetch(instructionBuffer, pc, program, loadStoreQueue):
    while instructionBuffer.isFull() is False and int(pc) < 4 * len(program) and pc != -1:
        for i in program:
            if i.adress == pc:
                instructionBuffer.add(i)
                # if (i.opname == 'Ld') or (i.opname == 'Sd'):                    # TODO: add LSQ in the FU
                #     loadStoreQueue.append(LoadStoreQueueEntry(pc, i.opname))
                if (i.opname == 'Bne') or (i.opname == 'Beq'):     # TODO: Branch prediction
                    pc = int(i.destination)
                else:
                    pc = pc + 4
                break
    return instructionBuffer, pc


def issue(reorderBuffer, instructionBuffer, pc, functionalUnit, architectureRegisterFile):
    if (instructionBuffer.head().opname == 'Ld') or (instructionBuffer.head().opname == 'Sd'):
        inst = instructionBuffer.pop()
        lsq = functionalUnit.findAvailableLSQ()      # TODO: does it need cycles?
        lsq.opName = inst.opname
        lsq.Vj = int(inst.source1)
        for register in architectureRegisterFile.intRegisterList:
            if register.name == inst.source2:
                if register.busy:
                    h = reorderBuffer.findLastEntry(register)
                    if h is not None and h.ready:
                        lsq.Vk = h.value
                    else:
                        lsq.Qk = h.name
                else:
                    lsq.Vk = register.value
                break

    if reorderBuffer.isFull() is False and pc != -1 and functionalUnit.isAvailable(instructionBuffer.head().opname):
        inst = instructionBuffer.pop()
        # fu = functionalUnit.findAvailable(inst.opname)   # if inst is a non ld/Sd instruction
        rs, fu_cycle = functionalUnit.findAvailable(inst.opname)
        find = False
        for register in architectureRegisterFile.intRegisterList:  # TODO: also need to check fp registers
            if register.name == inst.source1:
                if register.busy:
                    h = reorderBuffer.findLastEntry(register)
                    # for robEntry in ROB.list:
                    #     if robEntry.name == h:
                    #         if robEntry.ready:
                    if h is not None and h.ready:
                        # fu.reservationStation.Vj = h.value
                        rs.Vj = h.value
                    else:
                        # fu.reservationStation.Qj = h.name
                        rs.Qj = h.name
                else:
                    # fu.reservationStation.Vj = register.value     # TODO: check
                    rs.Vj = register.value     # TODO: check
                find = True
                break
        if not find:
            for register in architectureRegisterFile.fpRegisterList:
                if register.name == inst.source1:
                    if register.busy:
                        h = reorderBuffer.findLastEntry(register)
                        # for robEntry in ROB.list:
                        #     if robEntry.name == h:
                        #         if robEntry.ready:
                        if h is not None and h.ready:
                            # fu.reservationStation.Vj = h.value
                            rs.Vj = h.value
                        else:
                            # fu.reservationStation.Qj = h.name
                            rs.Qj = h.name
                    else:
                        # fu.reservationStation.Vj = register.value     # TODO: check
                        rs.Vj = register.value  # TODO: check
                    find = True
                    break
        if not find:
            rs.Vj = int(inst.source1)
            # for register in architectureRegisterFile.fpRegisterList:
            #     if register.name == inst.source1

        find = False
        for register in architectureRegisterFile.intRegisterList:
            if register.name == inst.source2:
                if register.busy:
                    h = reorderBuffer.findLastEntry(register)
                    # for robEntry in ROB.list:
                    #     if robEntry.name == h:
                    #         if robEntry.ready:
                    if h is not None and h.ready:
                        rs.Vk = h.value
                    else:
                        rs.Qk = h.name
                else:
                    rs.Vk = register.value
                find = True
                break
        if not find:
            for register in architectureRegisterFile.fpRegisterList:
                if register.name == inst.source2:
                    if register.busy:
                        h = reorderBuffer.findLastEntry(register)
                        # for robEntry in ROB.list:
                        #     if robEntry.name == h:
                        #         if robEntry.ready:
                        if h is not None and h.ready:
                            rs.Vk = h.value
                        else:
                            rs.Qk = h.name
                    else:
                        rs.Vk = register.value
                    find = True
                    break
        if not find:
            rs.Vk = int(inst.source2)

        b = reorderBuffer.createRobEntry(inst)

        if inst.destination != 'BGE':
            for register in architectureRegisterFile.intRegisterList:   # TODO: optimize
                if register.name == inst.destination:
                    if not register.busy:
                        register.robId = b
                        register.busy = True
                        break
            for register in architectureRegisterFile.fpRegisterList:
                if register.name == inst.destination:
                    if not register.busy:
                        register.robId = b
                        register.busy = True
                        break


        rs.destination = b
        rs.busy = True
        rs.opName = inst.opname
        rs.cyclesRemained = fu_cycle
    return reorderBuffer, instructionBuffer, functionalUnit, architectureRegisterFile


def execute(functionalUnit):
    for fu in functionalUnit.fuList:
        for rs in fu.reservationStation:
            if rs.busy and rs.Vj is not None:
                if rs.opName == 'LD':     # TODO: need a rs for load and store?
                    rs.cyclesRemained -= 1
                elif rs.Vk is not None:
                    rs.cyclesRemained -= 1
    return functionalUnit


def writeBack(commonDataBus, functionalUnit, reorderBuffer, architectureRegisterFile, instructionBuffer):
    commonDataBus.busy = False      # TODO: may have contention
    for fu in functionalUnit.fuList:
        ReservationStation = fu.reservationStation
        for rs in ReservationStation:
            if rs.cyclesRemained is not None and rs.busy is True:
                if rs.cyclesRemained <= 0 and not commonDataBus.busy:
                    rs.busy = False
                    if rs.opName != 'BGE':
                        result = rs.execute
                        b = rs.destination
                        commonDataBus.busy = True
                        commonDataBus.value = result
                        commonDataBus.address = b
                        for robentry in reorderBuffer.list:
                            if robentry.name == b:
                                robentry.value = result
                                robentry.ready = True
                                break
                        for fu2 in functionalUnit.fuList:
                            for rs2 in fu2.reservationStation:
                                # rs2 = fu2.reservationStation
                                if rs2.Qj == b:
                                    rs2.Vj = result
                                    rs2.Qj = None
                                if rs2.Qk == b:
                                    rs2.Vk = result
                                    rs2.Qk = None
                        rs.busy = False
                        rs.clear()
                    elif rs.opName == 'BGE':
                        if not rs.Vj >= rs.Vk:
                            listtoremove = reorderBuffer.flush(rs.destination)
                            functionalUnit.flush(listtoremove)
                            architectureRegisterFile.flush(listtoremove)
                            instructionBuffer.clear()

                            pc = -1
                        for e in reorderBuffer.list:
                            if e.name == rs.destination:
                                e.ready = True
                        rs.clear()
    return commonDataBus, functionalUnit, reorderBuffer, architectureRegisterFile, instructionBuffer


def commit(finished, pc, reorderBuffer, architectureRegisterFile):
    head = reorderBuffer.getHead()
    if head.opname == '':
        finished = True
        return finished, pc, reorderBuffer, architectureRegisterFile
    if head.ready:
        if head.opname == 'BGE':
            if pc == -1:
                finished = True     # TODO: stop sign should be redesigned
            reorderBuffer.pop()
        else:
            d = head.destination
            for reg in architectureRegisterFile.intRegisterList:
                if reg.name == d:
                    reg.value = head.value
                    if reg.robId == head.name:       # TODO: check the reset logic
                        reg.robId = None
                        reg.busy = False
                    index = reorderBuffer.head
                    for i in range(reorderBuffer.numelements - 1):
                        index += 1
                        index %= reorderBuffer.size
                        if reorderBuffer.list[index].destination == reg.name:
                            reg.robId = reorderBuffer.list[index].name
                            reg.busy = True
                            break

            for reg in architectureRegisterFile.fpRegisterList:
                if reg.name == d:
                    reg.value = head.value
                    if reg.robId == head.name:       # TODO: check the reset logic
                        reg.robId = None
                        reg.busy = False
                    index = reorderBuffer.head
                    for i in range(reorderBuffer.numelements - 1):
                        index += 1
                        index %= reorderBuffer.size
                        if reorderBuffer.list[index].destination == reg.name:
                            reg.robId = reorderBuffer.list[index].name
                            reg.busy = True
                            break

            reorderBuffer.pop()
    return finished, pc, reorderBuffer, architectureRegisterFile

