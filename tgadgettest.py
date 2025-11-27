import cirq
from tgadget import tGadget
from zerosim import AlwaysZeroSimulator
import numpy as np


q0, q1, q2, q3 = cirq.LineQubit.range(4)
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
    
    print("pass!")

circuit = cirq.Circuit(
    cirq.H(q0),
    cirq.CNOT(q0, q3),
    cirq.T(q1),
    cirq.T(q3),
    cirq.Y(q1),
    cirq.T(q2),
    cirq.X(q3),
    cirq.T(q2),
    cirq.M(q0)
)

print(circuit)

print("---------")
tg = tGadget(circuit)
tg.addTGadget()
newCir = tg.getCir()
print(newCir)
print("---------------")

print(circuit)

tgNew = tGadget(circuit)
tgNew.addMulitQubitMagicState()
newCir = tgNew.getCir()
print(newCir)

simulator = AlwaysZeroSimulator()


result = simulator.run(newCir, repetitions=100)

print(result)