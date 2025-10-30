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

def bitstringUnitary(bit_string):

    qubits = [cirq.LineQubit(i) for i in range(len(bit_string))]

    bitCircuit = cirq.Circuit()

    
    for i, bit in enumerate(bit_string):
        if bit == '1':
            bitCircuit.append(cirq.X(qubits[i]))
        else:
            bitCircuit.append(cirq.I(qubits[i]))
        
            
    return bitCircuit.unitary()

def B60():
    qubits = [cirq.LineQubit(i) for i in range(6)]
    circuitB60 = cirq.Circuit()

    for qubit in qubits:
        circuitB60.append(cirq.I(qubit))

    return circuitB60.unitary()

def B66():
    qubits = [cirq.LineQubit(i) for i in range(6)]
    circuitB66 = cirq.Circuit()
    for qubit in qubits:
        circuitB66.append(cirq.X(qubit))
    return circuitB66.unitary()

def E6():
    n = 6
    EvenBitStrings = []
    for i in range(2**n):
        bits = format(i, f'0{n}b')  
        if bits.count('1') % 2 == 0:
            EvenBitStrings.append(bits)

    unitarySum = np.zeros((2**6,2**6))
    for bitString in EvenBitStrings:
        unitarySum = unitarySum + bitstringUnitary(bitString)

    return unitarySum

def O6():
    n = 6
    OddBitStrings = []
    for i in range(2**n):
        bits = format(i, f'0{n}b')  
        if bits.count('1') % 2 == 1:
            OddBitStrings.append(bits)

    unitarySum = np.zeros((2**6,2**6))
    for bitString in OddBitStrings:
        unitarySum = unitarySum + bitstringUnitary(bitString)

    return unitarySum



#graphs
g1 = [(1,2),(2,3),(3,4),(4,5),(5,1),(1,6),(2,6),(3,6),(4,6),(5,6)]
g2 = [(1,2),(2,4),(4,5),(5,6),(6,1),(1,3),(2,3),(4,3),(5,3),(6,3)]


def K6():
    n = 6
    BitStrings = []
    for i in range(2**n):
        bits = format(i, f'0{n}b')  
        BitStrings.append(bits)

    unitarySum = np.zeros((2**6,2**6))
    for bitString in BitStrings:
        unitarySum = unitarySum + bitstringUnitary(bitString)


    I = np.eye(2)
    Z = np.array([[1, 0], [0, -1]])
    P0 = np.array([[1, 0], [0, 0]])
    P1 = np.array([[0, 0], [0, 1]])

    CZ_full = 0

    for k in range(0,5):
        for m in range(0,5):
            if k < m:

                for term in [(P0, I), (P1, Z)]:
                    op_list = []
                    for i in range(n):
                        if i == k:
                            op_list.append(term[0])  
                        elif i == m:
                            op_list.append(term[1]) 
                        else:
                            op_list.append(I)
                    
                    full_term = op_list[0]
                    for j in range(1, n):
                        full_term = np.kron(full_term, op_list[j])
                    CZ_full += full_term

    return CZ_full*unitarySum


def phi1():
    n = 6
    OddBitStrings = []
    for i in range(2**n):
        bits = format(i, f'0{n}b')  
        if bits.count('1') % 2 == 1:
            OddBitStrings.append(bits)

    unitarySum = np.zeros((2**6,2**6))
    for bitString in OddBitStrings:
        unitarySum = unitarySum + bitstringUnitary(bitString)


    I = np.eye(2)
    Z = np.array([[1, 0], [0, -1]])
    P0 = np.array([[1, 0], [0, 0]])
    P1 = np.array([[0, 0], [0, 1]])

    CZ_full = 0

    for (k,m) in g2:
                for term in [(P0, I), (P1, Z)]:
                    op_list = []
                    for i in range(n):
                        if i == k:
                            op_list.append(term[0])  
                        elif i == m:
                            op_list.append(term[1]) 
                        else:
                            op_list.append(I)
                    
                    full_term = op_list[0]
                    for j in range(1, n):
                        full_term = np.kron(full_term, op_list[j])
                    CZ_full += full_term

    print(CZ_full)
    print("=============")
    print(unitarySum)
    print("=============")
    return CZ_full*unitarySum



qubits = [cirq.LineQubit(i) for i in range(6)]
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
    MagicStateHGate().on_each(qubits)
)


################################

qubits = [cirq.LineQubit(i) for i in range(2)]

circuit = cirq.Circuit(
    cirq.H(qubits[0]),
    cirq.X(qubits[1]),
    cirq.CX(qubits[0],qubits[1]),
)
print("==========")
print(bitstringUnitary('10'))
print("==========")
print(bitstringUnitary('01'))
print("==========")
print(circuit.unitary()/0.70710678)
print("==========")
print("==========")
print(phi1())
###################################
print(circuit)
oldUnitary = circuit.unitary()

print(oldUnitary)

newUnitary = oldUnitary


compareUnitary(newUnitary,oldUnitary)


