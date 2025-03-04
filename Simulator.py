#Use these variables to load/read values in register
x0 = 0
x1 = 0
x2 = 0
x3 = 0
x4 = 0
x5 = 0
x6 = 0
x7 = 0
x8 = 0
x9 = 0
x10 = 0
x11 = 0
x12 = 0
x13 = 0
x14 = 0
x15 = 0
x16 = 0
x17 = 0
x18 = 0
x19 = 0
x20 = 0
x21 = 0
x22 = 0
x23 = 0
x24 = 0
x25 = 0
x26 = 0
x27 = 0
x28 = 0
x29 = 0
x30 = 0
x31 = 0

#Global Variables
RD1 = 0
RD2 = 0
immExt = ""
ALUResult = ""
PCNext=0
zero = False #flag for b-type instruction
registers = {"00000" : x0, "00001" : x1, "00010" : x2, "00011" : x3, "00100" : x4, "00101" : x5, "00110" : x6, "00111" : x7, "01000" : x8, "01001" : x9, "01010" : x10, "01011" : x11, "01100" : x12, "01101" : x13, "01110" : x14, "01111" : x15, "10000" : x16, "10001" : x17, "10010" : x18, "10011" : x19, "10100" : x20, "10101" : x21, "10110" : x22, "10111": x23, "11000" : x24, "11001" : x25, "11010" : x26, "11011" : x27, "11100" : x28, "11101" : x29, "11110" : x30, "11111": x31}
def Instruction_Memory(inst):
	instr={"op":inst[25:32],"func3":inst[17:20],"func7":inst[1],"A1":inst[12:17],"A2":inst[7:12],"A3":inst[20:25],"Extend":inst[0:25]}
def PCNext(PCSrc,immExt,PC):
	global PCNext
	if PCSrc==1:
		PCNext=PC+int(immExt,2)
	elif PCSrc==0:
		PCNext=PC+4
	return PCNext
	
def mux(input1,input2,input3,ch1):
	if(ch1=='00'):
		return input1
	elif(ch1=='01'):
		return input2
	else:
		return input3
		
def signed(inp):
	#signed integer representation of binary
	if (inp[0] == '1'): #represents 2's complement
		new = ""
		for i in inp: #flip the bits
			if i == '1':
				new += '0'
			else: new += '1'
		return -(int(new, 2) + 1)
	else:
		return int(new, 2)
		
def register_file(A1, A2, A3, WD3, WE3, clk=True):
	global RD1, RD2, registers
	RD1 = registers[A1]
	RD2 = registers[A2]
	
	if (WE3 == 1): registers[A3] = int(WD3, 2)

def extend(inp, immSrc):
	#31:7
	global immExt
	if (immSrc == "00"): #l instruction
		immExt = inp[0:12][::-1]
	elif (immSrc == "01"): #s instruction
		immExt = inp[20::-1] + inp[0:7]
	elif (immSrc == "10"): #b instruction
		immExt = inp[0] + inp[1:8] + inp[19:23] + inp[23] + '0'
	else: #j instruction
		immExt = inp[0] + inp[12:20] + int[11] + inp[1:11] + '0'

def ALU(SrcA, SrcB, ALUCont, ALUSrc):
	global immExt, ALUResult, zero
	immExt = "" #initialise both to empty
	ALUResult = ""
	
	if (ALUSrc == '0'): #choosing between RD2 and immExt
		SrcB = RD2
	else:
		SrcB = immExt
		
	if (ALUCont == "000"): #add
		ALUResult = str(int(SrcA) + int(SrcB))
	elif (ALUCont == "001"): #subtract
		ALUResult = str(int(SrcA) - int(SrcB))
	elif (ALUCont == "010"): #bitwise_and
		for i, j in SrcA, SrcB:
			ALUResult += str(int(i, 2) & int(j, 2))
	elif (ALUCont == "011"): #bitwise_or
		for i, j in SrcA, SrcB:
			ALUResult += str(int(i, 2) | int(j, 2))
	elif (ALUCont == "101"): #set less than
		if (signed(SrcA) < signed(SrcB)): ALUResult = '1'
		else: ALUResult = '0'
