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
              return self.RecDecompGate(self.cirT, i, cirq.I) + self.RecDecompGate(self.cirT, i, cirq.Z)
        
        raise Exception("no T gate found.") 

    def RecDecompGate(self, newCir, pos, gate, phase = 1):

        tempPhaseCir = self.replaceTgates(newCir, pos, gate)
        newPhase = phase * tempPhaseCir.getPhase()
        for i in range(len(tempPhaseCir.getCir())):
            if self.foundTgateInMoment(tempPhaseCir.getCir()[i]):
              print("starting T gate decomposition into (aI + bZ).")
              return self.RecDecompGate(tempPhaseCir.getCir(), i, cirq.I, newPhase) + self.RecDecompGate(tempPhaseCir.getCir(), i, cirq.Z, newPhase)
        tempPhaseCir.setPhase(newPhase)
        return [tempPhaseCir]
    

    def replaceTgates(self, cir, pos, gate):

        new_moments = []
        if isinstance(gate, cirq.ZPowGate):
            phase = (1 - np.exp(1j*(np.pi/4)))/2
        elif isinstance(gate, cirq.IdentityGate):
            phase = (1 + np.exp(1j*(np.pi/4)))/2

        else:
            raise Exception("wrong gate as an input. Only I and Z gates are accepted")
        
        for i in range(len(cir)):

            if i == pos:
                moment = self.switchMoment(cir[i],gate)

                new_moments.append(moment)

            else:
                new_moments.append(cir[i])
        return PhaseCircuit(phase, cirq.Circuit(new_moments))

    def foundTgateInMoment(self,moment):
        for operation in moment:
                if isinstance(operation.gate, cirq.ZPowGate):
                    if operation.gate.exponent == 0.25:
                        return True
        return False


    def switchMoment(self, moment, gate):
        new_ops = []
        numOfTgates = 0
        for op in moment:
            
            if isinstance(op.gate, cirq.ZPowGate):
                    if op.gate.exponent == 0.25 and numOfTgates == 0:
                        new_ops.append(gate(op.qubits[0]))
                        numOfTgates = 1
                        continue

            new_ops.append(op)
        
        return cirq.Moment(new_ops)
    
    
class PhaseCircuit():
    def __init__(self,phase,cir):
        if isinstance(cir, cirq.Circuit):
            self.cir = cir
            self.phase = phase
        else:
            raise TypeError("not a cirq.Circuit object!")
        
    def getCir(self):
        return self.cir

    def getPhase(self):
        return self.phase
    def setPhase(self,phase):
        self.phase = phase




                    

                

    
