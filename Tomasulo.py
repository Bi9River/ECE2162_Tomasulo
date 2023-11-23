from LoadStoreQueue import LoadStoreQueue


def fetch(instructionBuffer, pc, program):
    while instructionBuffer.isFull() is False and int(pc) < 4 * len(program) and pc != -1:
        for i in program:
            if i.adress == pc:
                instructionBuffer.add(i)
                # if (i.opname == 'Ld') or (i.opname == 'Sd'):                    # TODO: add LSQ in the FU
                #     loadStoreQueue.append(LoadStoreQueueEntry(pc, i.opname))
                if (i.opname == 'Bne') or (i.opname == 'Beq'):  # TODO: Branch prediction
                    pc = int(i.destination)
                else:
                    pc = pc + 4
                break
    return instructionBuffer, pc


def issue(reorderBuffer, instructionBuffer, pc, functionalUnit, architectureRegisterFile):
    if reorderBuffer.isFull() is False and pc != -1:
        if (instructionBuffer.head().opname == 'Ld') or (instructionBuffer.head().opname == 'Sd'):
            inst = instructionBuffer.pop()
            lsq = functionalUnit.findAvailableLSQ()  # TODO: does it need cycles?
            lsq.opName = inst.opname
            lsq.Vj = int(inst.source1)
            for register in architectureRegisterFile.intRegisterList:  # TODO: source is int and destination is fp
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
            b = reorderBuffer.createRobEntry(inst)
            for register in architectureRegisterFile.intRegisterList:  # TODO: optimize
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

            lsq.destination = b
            lsq.busy = True
            lsq.opName = inst.opname
            lsq.cyclesRemained = 4

        elif functionalUnit.isAvailable(instructionBuffer.head().opname):  # TODO: LD also goes into this part
            inst = instructionBuffer.pop()
            # fu = functionalUnit.findAvailable(inst.opname)   # if inst is a non ld/Sd instruction
            rs, fu_cycle = functionalUnit.findAvailableRS(inst.opname)
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
                        rs.Vj = register.value  # TODO: check
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
                            # fu.reservationStation.Vj = register.value
                            rs.Vj = register.value
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

            b = reorderBuffer.createRobEntry(inst)  # TODO: LD and SD also go into ROB(unless it can solve immediately?)
            # TODO: Also check the condition for creating ROB entry
            if inst.destination != 'Bne' and inst.destination != 'Beq':
                for register in architectureRegisterFile.intRegisterList:  # TODO: optimize
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


def execute(functionalUnit, memory):
    for fu in functionalUnit.fuList:
        for rs in fu.reservationStation:
            if rs.busy and rs.Vj is not None:
                if rs.opName == 'LD':  # TODO: need a rs for load and store?
                    rs.cyclesRemained -= 1
                elif rs.Vk is not None:
                    rs.cyclesRemained -= 1  # TODO: Ld and Sd
        for lsq in fu.loadstorequeue:
            if lsq.busy and lsq.Vj is not None and lsq.Vk is not None:
                lsq.address = lsq.Vj + lsq.Vk
                if lsq.opName == 'Ld':
                    lsq.value = memory.getValue(lsq.address)
                if lsq.opName == 'Sd':
                    memory.setValue(lsq.address, lsq.Vk)
    return functionalUnit


def memoryAccess(functionalUnit, memory):
    for fu in functionalUnit.fuList:
        for lsp in fu.loadstorequeue:
            if lsp.busy and lsp.Vj is not None and lsp.Vk is not None:
                lsp.cyclesRemained -= 1
    return functionalUnit, memory


def writeBack(commonDataBus, functionalUnit, reorderBuffer, architectureRegisterFile, instructionBuffer):
    commonDataBus.busy = False  # TODO: may have contention
    for fu in functionalUnit.fuList:
        LoadStoreQueue = fu.loadstorequeue
        for lsq in LoadStoreQueue:
            if (lsq.cyclesRemained is not None) and (lsq.busy is True):
                if lsq.cyclesRemained <= 0:
                    lsq.busy = False
                    if lsq.opName == 'Ld':
                        commonDataBus.busy = True
                        commonDataBus.value = lsq.value
                        commonDataBus.address = lsq.destination
                        for robentry in reorderBuffer.list:
                            if robentry.name == lsq.destination:
                                robentry.value = lsq.value
                                robentry.ready = True
                                break
                        for fu2 in functionalUnit.fuList:
                            for lsq2 in fu2.loadstorequeue:
                                if lsq2.Qj == lsq.destination:
                                    lsq2.Vj = lsq.value
                                    lsq2.Qj = None
                                if lsq2.Qk == lsq.destination:
                                    lsq2.Vk = lsq.value
                                    lsq2.Qk = None
                        lsq.busy = False
                        # lsq.clear()
                    elif lsq.opName == 'Sd':
                        commonDataBus.busy = True
                        commonDataBus.value = lsq.Vk
                        commonDataBus.address = lsq.destination
                        for robentry in reorderBuffer.list:
                            if robentry.name == lsq.destination:
                                robentry.value = lsq.Vk
                                robentry.ready = True
                                break
                        for fu2 in functionalUnit.fuList:
                            for lsq2 in fu2.loadstorequeue:
                                if lsq2.Qj == lsq.destination:
                                    lsq2.Vj = lsq.Vk
                                    lsq2.Qj = None
                                if lsq2.Qk == lsq.destination:
                                    lsq2.Vk = lsq.Vk
                                    lsq2.Qk = None
                        lsq.busy = False
                        lsq.clear()
        ReservationStation = fu.reservationStation
        for rs in ReservationStation:
            if rs.cyclesRemained is not None and rs.busy is True:
                if rs.cyclesRemained <= 0 and not commonDataBus.busy:
                    rs.busy = False
                    if rs.opName != 'Bne' or rs.opName != 'Beq':
                        result = rs.execute()
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
                    elif rs.opName == 'Bne' or rs.opName == 'Beq':
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

        # loadStoreQueue = fu.loadstorequeue
        # for lsq in loadStoreQueue:     # TODO: write back the value to ROB

    return commonDataBus, functionalUnit, reorderBuffer, architectureRegisterFile, instructionBuffer


def commit(finished, pc, reorderBuffer, architectureRegisterFile, cycle):
    head = reorderBuffer.getHead()
    if head.opname == '' and cycle > 1:
        finished = True
        return finished, pc, reorderBuffer, architectureRegisterFile
    if head.ready:
        if head.opname == 'Bne' or head.opname == 'Beq':
            if pc == -1:
                finished = True  # TODO: stop sign should be redesigned
            reorderBuffer.pop()
        else:
            d = head.destination
            for reg in architectureRegisterFile.intRegisterList:
                if reg.name == d:
                    reg.value = head.value
                    if reg.robId == head.name:  # TODO: check the reset logic
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
                    if reg.robId == head.name:  # TODO: check the reset logic
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
