import cirq
from decompCircuit import DecompCircuit
import numpy as np


q0, q1, q2, q3 = cirq.LineQubit.range(4)

circuit = cirq.Circuit(
    cirq.H(q0),
    cirq.CNOT(q0, q3),
    cirq.T(q1),
    cirq.T(q3),
    cirq.Y(q1),
    cirq.T(q2)
)
print(circuit)

newCir = DecompCircuit(circuit)
Iphi, Zphi = newCir.decomp()
print(Iphi[0])
print(Iphi[1])
print(Zphi[0])
print(Zphi[1])