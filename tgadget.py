import cirq
import numpy as np

class tGadget():
    def __init__(self,cir):
        if isinstance(cir, cirq.Circuit):
            self.cir = cir
            self.NoQubits = len(cir.all_qubits())
        else:
            raise TypeError("not a cirq.Circuit object!")

    def getCir(self):
        print("return Tgadget circuit")
        return self.cir
    

    def addTGadget(self):
        print(self.cir[1])
 
        i = 0
        while(i<len(self.cir)):
            print("+++++")
            print(i)

            for n in range(self.numOfTGatesInMoment(self.cir[i])):
                self.initTgadget(i)
                print(f"init T at i{i}")

            i+=1
         

                


    def numOfTGatesInMoment(self,moment):
        totalTGates = 0
        for operation in moment:
                print(f"operation: {operation}")
                if isinstance(operation.gate, cirq.ZPowGate) and (operation.qubits[0].x < self.NoQubits):
                    if operation.gate.exponent == 0.25:
                        totalTGates+=1
        return totalTGates

    

    def switchMoment(self, moment, ancilla):
        numOfTgates = 0
        prevOps = []
        nextOps = []
        for op in moment:
            found = False
            if isinstance(op.gate, cirq.ZPowGate) and (op.qubits[0].x < self.NoQubits):
                    if op.gate.exponent == 0.25 and numOfTgates == 0:
                        m1 = cirq.Moment(cirq.H(ancilla))    
                        m2 = cirq.Moment(cirq.T(ancilla))                             #ToDo
                        m3 = cirq.Moment(cirq.CX(op.qubits[0], ancilla))
                                    #need alternative?
                        m4 = cirq.Moment(cirq.measure(ancilla, key = 'm'),cirq.S(op.qubits[0]).with_classical_controls('m'))
                        numOfTgates = 1
                        found = True
                        continue
            
            if found:
                nextOps.append(op)
            else:
                prevOps.append(op)
        if numOfTgates > 0:
            return [cirq.Moment(prevOps), m1, m2, m3, m4, cirq.Moment(nextOps)]
        else:
            raise Exception

    def initTgadget(self,pos):

        new_moments = []

        resourceQubit = cirq.LineQubit(len(self.cir.all_qubits()))

        
        for i in range(len(self.cir)):

            if i == pos:
                moments = self.switchMoment(self.cir[i],resourceQubit)
                for m in moments:
                    new_moments.append(m)

            else:
                new_moments.append(self.cir[i])
        self.cir = cirq.Circuit(new_moments)

