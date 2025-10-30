import cirq
from decompCircuit import DecompCircuit
import numpy as np

class MagicStateHGate(cirq.Gate):
    def __init__(self):
        super().__init__()

    def num_qubits(self):
        return 1  

    def _unitary_(self):
        return np.array([[1, 0],
                         [0, np.tan(np.pi/8)]])

    def __repr__(self):
        return 'MagicStateHGate()'


q0, q1, q2, q3, q4, q5 = cirq.LineQubit.range(6)
def compareUnitary(u1,u2):
    #print(u1)
    #print(u2)
    if len(u1) != len(u2):
        print("Size difference in unitaries.")
        return

    for i in range(len(u1)):
        for j in range (len(u1)):
          if not np.isclose(u1[i][j], u2[i][j], rtol=1e-15, atol=1e-15):
            print("fail.")
            print(u1[i][j])
            print(u2[i][j])
            return 
    
    #print("pass!")

circuit = cirq.Circuit(
    MagicStateHGate().on_each(q0, q1, q2, q3, q4, q5)
)

print(circuit)
oldUnitary = circuit.unitary()

print(oldUnitary)


newUnitary = oldUnitary


compareUnitary(newUnitary,oldUnitary)

