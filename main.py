from collections import deque
from ReadFile import *
from Tomasulo import *
from Instruction import Instruction, InstructionBuffer
from ReservationStation import ReservationStation
from RegisterFile import RegisterFile
from FunctionalUnit import FunctionalUnit, FunctionalUnits
from CommonDataBus import CommonDataBus
from ReorderBuffer import ReorderBuffer
from Memory import Memory
from LoadStoreQueue import LoadStoreQueue
# from Register import Register


def print_report():
    global cycles
    report_file = open("Report.txt", "a")
    report_file.write("------------------------\n")
    report_file.write("CYCLE " + str(cycles) + '\n\n')
    report_file.write(IB.toString() + '\n')
    report_file.write(RF.toString() + '\n')
    report_file.write(FU.toString() + '\n')
    report_file.write(ROB.toString() + '\n')
    report_file.write(CDB.toString() + '\n')
    report_file.close()


PC = 0
number_of_registers = 0
instruction_window_size = 0
program = []
LSQ = []
finished = False


number_of_registers, instruction_window_size, rs_size_dict = readParametersFile()
MM = Memory()
FU = FunctionalUnits()
CDB = CommonDataBus()
FU = readUnitsFile(FU, rs_size_dict)
program = readProgramFile(program)

IB = InstructionBuffer(instruction_window_size)
RF = RegisterFile(number_of_registers)
ROB = ReorderBuffer(len(FU.fuList))
cycles = 1
rf = open("Report.txt", "w")
rf.close()

while (not finished) and (PC != -1):
    CDB, FU, ROB, RF, IB = writeBack(CDB, FU, ROB, RF, IB)
    finished, PC, ROB, RF = commit(finished, PC, ROB, RF, cycles)
    IB, PC = fetch(IB, PC, program)
    if not IB.isEmpty():
        ROB, IB, FU, RF = issue(ROB, IB, PC, FU, RF)    # delete output PC
    FU = execute(FU, MM)
    print_report()
    cycles += 1


if finished:
    print('R2:', RF.intRegisterList[2].value)
    print('F5:', RF.fpRegisterList[5].value)
