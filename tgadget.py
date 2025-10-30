import cirq
import numpy as np

class tGadget():
    def __init__(self,cir):
        if isinstance(cir, cirq.Circuit):
            self.cir = cir
        else:
            raise TypeError("not a cirq.Circuit object!")

    def getCir(self):
        print("return Tgadget circuit")
        return self.cir
    

    def addTGadget(self):
        rangetemp = len(self.cir)
        for i in range(rangetemp):
            print(i)
            if self.foundTgateInMoment(self.cir[i]):
            
                print("adding T gadget.")
                self.initTgadget(i)
        

    

    def switchMoment(self, moment, ancilla):
        new_ops = []
        numOfTgates = 0
        prevOps = []
        nextOps = []
        for op in moment:
            found = False
            if isinstance(op.gate, cirq.ZPowGate):
                    if op.gate.exponent == 0.25 and numOfTgates == 0:
                        m1 = cirq.Moment(cirq.T(ancilla))                             #ToDo
                        m2 = cirq.Moment(cirq.CX(op.qubits[0], ancilla))
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
            return [cirq.Moment(prevOps), m1, m2,  m4 ,cirq.Moment(nextOps)]
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

    def foundTgateInMoment(self,moment):
        for operation in moment:
                if isinstance(operation.gate, cirq.ZPowGate):
                    if operation.gate.exponent == 0.25:
                        return True
        return False