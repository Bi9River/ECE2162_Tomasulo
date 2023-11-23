# Tomasulo-Algorithm
   Implemented dynamic scheduling of instructions using Tomasulo's algorithm with reorder buffer in python

### Parameters
Size of the instruciton window and number of registers can be configured using **Parameters.txt** file.

**Default Values**
```
number_of_registers: 4
instruction_window_size: 4
```

### Functional Units
Functional units can be configured using **Units.txt** file.

**Default Values**
```
0: ADD,SUB 1 # ADD/SUB UNIT
1: MUL 4     # MUL UNIT
2: MUL 4     # MUL UNIT
3: DIV 4     # DIV UNIT
4: LD,BGE 1  # INTEGER UNIT
```

### The program
Put the assembly program you want to execute in **Program.txt**.


**Default Program**
"This program implements Newton's algorithm to compute a root of the function x^2-2x+1.
x is initalized to 0 and four iterations are performed to successively improve the approximation.
The loop begins at address 4 and ends at address 36.
After four iterations, the value of x becomes equal to 0.9375, which is stored in register R0."

```
0:  LD  R0, 0
4:  MUL R2, R0, 2
8:  MUL R1, R0, R0
12: SUB R3, R1, R2
16: DIV R1, 1, 16
20: SUB R2, R2, 2
24: ADD R3, R3, 1
28: DIV R2, R3, R2
32: SUB R0, R0, R2 
36: BGE R3, R1, 4
```
### The output
**Example output**
```
------------------------
CYCLE 0

Instruction Window
LD R0, 0.0
ADD R2, R1, R0
SUB R1, R2, 1
MUL R2, R1, 2

Registers
R0: -   ROB0
R1: -   ROB1
R2: -   -
R3: -   -

Reservation Stations
RS0: ADD 0.0  1.0  ROB0  
RS1: MUL 2.0  3.0  ROB1
RS2:  
RS3:
RS4:

Reorder Buffer
ROB0: ADD R0 - (H)
ROB1: MUL R1 - (T)
ROB2:
ROB3:
ROB4:

Common Data Bus
6.0 ROB1

------------------------
CYCLE 1
```



