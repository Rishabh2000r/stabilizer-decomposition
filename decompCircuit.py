import cirq
import numpy as np

class DecompCircuit:
    def __init__(self,cir):
        if isinstance(cir, cirq.Circuit):
            self.cirT = cir
            
        else:
            raise TypeError("not a cirq.Circuit object!")
    

    def decomp(self):
        for i in range(len(self.cirT)):
            
            if self.foundTgateInMoment(self.cirT[i]):
                print("starting T gate decomposition into (aI + bZ).")
                return (self.replaceTgates(self.cirT, cirq.I), self.replaceTgates(self.cirT, cirq.Z) )
        raise Exception("no T gate found.")

    
    def foundTgateInMoment(self,moment):
        for operation in moment:
                if isinstance(operation.gate, cirq.ZPowGate):
                    if operation.gate.exponent == 0.25:
                        return True
        return False

    def replaceTgates(self, cir, gate):
        sumOfTgates = 0
        new_moments = []
        if isinstance(gate, cirq.ZPowGate):
            phase = (1 - np.exp(1j*(np.pi/4)))/2
        elif isinstance(gate, cirq.IdentityGate):
            phase = (1 + np.exp(1j*(np.pi/4)))/2

        else:
            raise Exception("wrong gate as an input. Only I and Z gates are accepted")
        
        for i in range(len(cir)):
            numOfTgates, moment = self.switchMoment(cir[i],gate)
            sumOfTgates = sumOfTgates + numOfTgates
            new_moments.append(moment)

        return phase**sumOfTgates, cirq.Circuit(new_moments)

    def switchMoment(self, moment, gate):
        new_ops = []
        numOfTgates = 0
        for op in moment:
            
            if isinstance(op.gate, cirq.ZPowGate):
                    if op.gate.exponent == 0.25:
                        new_ops.append(gate(op.qubits[0]))
                        numOfTgates = numOfTgates + 1
                        continue

            new_ops.append(op)
        
        return numOfTgates, cirq.Moment(new_ops)

                        
        







                    

                

    
