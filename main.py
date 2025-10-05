import cirq
from decompCircuit import DecompCircuit
import numpy as np


q0, q1, q2, q3 = cirq.LineQubit.range(4)
def compareUnitary(u1,u2):
    print(u1)
    print(u2)
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
    
    print("pass!")

circuit = cirq.Circuit(
    cirq.H(q0),
    cirq.CNOT(q0, q3),
    cirq.T(q1),
    cirq.T(q3),
    cirq.Y(q1),
    cirq.T(q2)
)

test = (1 + np.exp(1j*(np.pi/4)))/2
print(test**2)

oldUnitary = circuit.unitary()


newCir = DecompCircuit(circuit)
listPhaseCircuits = newCir.decomp()
lenOldUnit = len(listPhaseCircuits[0].getCir().unitary())
newUnitary = np.zeros((lenOldUnit,lenOldUnit))

print("________________________")
for pc in listPhaseCircuits:
    print(pc.getPhase())
    print(pc.getCir())

    newUnitary = newUnitary + (pc.getPhase()*pc.getCir().unitary())

    print("________________________")


compareUnitary(newUnitary,oldUnitary)